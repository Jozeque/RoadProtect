# 00 — Bot Spec Overview & Framework

*Read this first. Every scenario file references the concepts defined here. If a scenario contradicts this doc, this doc wins.*

**Version**: 0.1 (draft)
**Last updated**: 2026-05-26
**Audience**: the new bot vendor's product / engineering team

---

## 0.0 Critical companion: CRM integration

The bot **reads from and writes to the Road Protect CRM**. The CRM is the source of truth for every user attribute used in trigger predicates (`מנוי נוכחי`, `מקור הגעה`, `קנסות פעילים`, `סנטימנט AI`, etc.).

Before implementing any trigger predicate or branch logic in this doc, read **`10_crm_integration.md`** end-to-end. It covers: the 19 CRM columns, the 3 enum value sets, the field-by-field mapping from bot-spec variables to CRM columns, the lead-warmth scoring model, the bot's write-back contract, and the read-freshness SLAs.

The shorthand `user.subscription = 'trademobile_free'` in scenarios `01_*` through `07_*` is convenience notation — the real implementation reads `מנוי נוכחי = "Trial (Trademobile)"` from the CRM per `10_crm_integration.md` § 10.3.

---

## 0.1 What we are building

Two WhatsApp agents:

- **C2B agent (outbound).** Initiates conversations with prospects, free-tier users, lapsed users, and expiring-soon users at specific lifecycle moments. Sequences of 1–3 touches per scenario, with explicit timing and exit conditions.
- **B2C agent (inbound).** Responds to users who message Road Protect's WhatsApp number themselves. Single intent-router with sub-flows.

Both agents share: knowledge base, voice/tone, personas, escalation rules, legal-line.

There are **7 C2B scenarios (C1–C7)** and **1 B2C scenario (B1)** in scope this round. New scenarios go through the normal idea → spec pipeline, not into this spec.

---

## 0.2 State machine — per user, per scenario

Every (user × scenario) pair has a status. Possible values:

| Status | Meaning |
|---|---|
| `eligible` | Trigger predicate satisfied, scenario not yet entered. Sitting in queue. |
| `suppressed` | Eligible but blocked by suppression matrix (another scenario takes priority). |
| `entered` | Touch 1 has been sent. Awaiting reply or next touch. |
| `replied` | User replied at least once. Bot is now in conversation mode (branches, B1 intent routing for inbound). |
| `converted` | User performed the scenario's success action (subscribed / upgraded / appealed). Sequence ends, scenario marked won. |
| `opted_out` | User triggered opt-out phrase or clicked unsubscribe. Sequence ends. Global opt-out applied (all scenarios cancelled for this user). |
| `escalated` | Bot handed off to human. Sequence pauses (does not end). Resumes only if human flags it as resumable. |
| `exhausted` | All planned touches sent, no reply, no conversion. Sequence ends, scenario marked lost-no-reply. |
| `expired` | Trigger window passed (e.g. fine paid before C5 could close). Sequence ends, scenario marked lost-stale. |
| `undeliverable` | WhatsApp delivery failed permanently (invalid number, user blocked the business number). Sequence ends. |

Transitions are one-way except `entered → replied`, `replied → converted`, and `escalated → entered` (rare).

**Every state transition emits an event** (see `dashboard-spec/02_event_schema.md`).

---

## 0.3 Trigger predicates — how to write them

Every scenario specifies its trigger as a **predicate**, not prose. The predicate is the boolean condition the orchestrator evaluates to set a user to `eligible`.

Format used throughout `bot-spec/`:

```
TRIGGER (C5 — free user got a fine):
  user.subscription IN ('detection', 'trademobile_free')
  AND fine.detected_at >= NOW() - INTERVAL '30 minutes'
  AND fine.status = 'new'
  AND user.opted_out = FALSE
  AND user.last_outbound_at <= NOW() - INTERVAL '24 hours'
```

If the vendor can't translate the predicate into a query against their data source, the trigger is too vague — flag it in clarification.

---

## 0.4 Multi-touch sequence model

A scenario sequence is an ordered list of touches. Each touch specifies:

1. **Delay from previous step** — for touch 1, from `eligible` moment; for touch 2+, from the previous touch's send time.
2. **Skip conditions** — when this touch is *not* sent even if the timer fires (e.g. user replied → skip touch 2's "did you see my message?" copy and let inbound branches handle it).
3. **Exit conditions** — when the whole sequence ends after this touch (e.g. converted, opted out).
4. **Variants** — A/B slots. Vendor picks one at random if multiple defined, logs which.
5. **Events emitted** — canonical event names per `dashboard-spec/02_event_schema.md`.

**Default touch cadence (used as a baseline, overridden per scenario):**

| Touch | Delay from prev | Purpose |
|---|---|---|
| 1 | 0 | Opener |
| 2 | +48h | Light nudge if no reply ("ראיתי שלא ענית — האם זה הזמן הלא נכון?") |
| 3 | +5 days | Final value reframe / soft exit |

After touch 3 with no reply: sequence enters `exhausted`. No more outbound for this scenario for **6 months** unless trigger predicate fires again on a *new* event.

---

## 0.5 Suppression matrix — who wins when a user is eligible for two scenarios

If a user qualifies for multiple scenarios simultaneously, only one fires. Priority order:

| Priority | Scenario | Reasoning |
|---|---|---|
| 1 (highest) | **C5** (free user got fine) | Time-sensitive, user-friction-saving. Always fires first. |
| 2 | **C7** (dirty winback w/ coupon) | Has a clear close-step; should not be delayed. |
| 3 | **C4** (Trademobile welcome) | Onboarding moment — fires once per user, never repeated. |
| 4 | **C6** (pre-expiry retention) | Calendar-driven, can wait if a higher-priority scenario is active. |
| 5 | **C2** (Trademobile active w/ fines) | Active-user upsell — not urgent vs. fresh fine. |
| 6 | **C3** (past customer winback) | Reactivation — least time-sensitive. |
| 7 (lowest) | **C1** (cold) | Lowest yield, lowest priority. |

**Rules:**
- Only one C2B scenario can be `entered` per user at a time. If user is in C2 and C5 trigger fires, C2 is paused and C5 takes over. C2 resumes only if C5 closes without conversion.
- B1 (inbound) is orthogonal — always responds to inbound regardless of outbound state.
- A user in `replied` or `escalated` state on any scenario is suppressed from all other outbound until resolved.

---

## 0.6 Frequency caps

Hard limits applied globally per user, regardless of scenario:

- **Max 1 outbound message every 24h** (rolling window).
- **Max 3 outbound messages every 7 days** (rolling window).
- **Max 8 outbound messages every 30 days** (rolling window).

If a planned touch would violate a cap, **defer** (don't drop) the touch until the cap window opens. If deferral pushes past the scenario's expiry window, mark `expired` and don't send.

These caps protect against the bot becoming spammy when a user qualifies for multiple back-to-back triggers.

---

## 0.7 Quiet hours

No outbound messages sent during:

- **Weekday nights**: 22:00 → 08:00 Asia/Jerusalem
- **Friday evening to Saturday evening**: 17:00 Friday → 21:00 Saturday Asia/Jerusalem (Shabbat)
- **Major Israeli holidays** (Yom Kippur, Rosh Hashanah day-of, Pesach erev + day 1, Sukkot day 1, Shavuot, Yom HaAtzmaut, Yom HaZikaron): no outbound

Touches scheduled inside a quiet window are deferred to the next eligible window's open. They are not dropped (except per the frequency cap rule above).

**Inbound** is always answered, including in quiet windows — the user reached out, we respond.

---

## 0.8 Opt-out

**Trigger phrases** (case-insensitive, partial match):

- "הסר אותי" / "להסיר" / "תסיר"
- "לא לפנות שוב" / "אל תפנו" / "אל תפנה"
- "stop" / "unsubscribe"
- "להפסיק לקבל הודעות" / "להפסיק"
- "להוריד מהרשימה"

When a trigger phrase is detected on any message from the user (to either C2B or B1):

1. Set `user.opted_out = TRUE` immediately.
2. Cancel all in-flight sequences for the user (all C2B scenarios → status `opted_out`).
3. Send acknowledgment: *"הוסרת מרשימת התפוצה. לא נשלח אליך הודעות נוספות. אם תרצה לחזור — תמיד אפשר ליצור קשר בכתובת [link]."*
4. Emit `user.opted_out` event with reason = `user_request`.
5. User remains opted-out permanently until they message in themselves AND explicitly request to be re-added.

**Edge case**: if user says "לא עכשיו" or "לא בטוח" — **not** an opt-out. That's hesitation; sequence continues per branch logic.

---

## 0.9 Gender detection

Default to **gender-neutral** verb forms ("ברצונך", "עבורך", "שלך", "תוכל/י") in touch 1.

After user's first reply:

| Signal | Action |
|---|---|
| Reply contains masculine 1st-person verb ("מעוניין", "אני יודע", "אני רוצה" + masculine adjective like "מעוניין", "סגור") | Lock masculine for rest of conversation. |
| Reply contains feminine 1st-person verb ("מעוניינת", "אני יודעת", "אני רוצה" + feminine adjective like "מעוניינת", "סגורה") | Lock feminine. |
| Ambiguous reply (just "כן" / "תשלח לי") | Stay neutral. Re-evaluate on next reply. |

**Per-scenario message variants** are written in both masculine and feminine where the natural Hebrew reads awkwardly without gender. Don't use slash-forms ("מעוניין/ת") inside warm/emotional copy — it kills warmth.

---

## 0.10 AI disclosure

The bot identifies as AI when:

- User asks: "מי אתה?", "אתה בנאדם?", "אתה אמיתי?"
- Bot is in cold-outreach scenarios (C1, C3) — disclosure inside touch 1's signature: *"אני סוכן AI דיגיטלי"*
- User has been talking to bot for >5 turns and hasn't been told yet — opportunistically disclose on a natural beat

The bot does **not**:

- Proactively pretend to be human
- Lie when asked
- Use a human persona name (no "אני יוסי") — always "אני העוזר הדיגיטלי של Road Protect" or "אני סוכן AI דיגיטלי"

---

## 0.11 Legal line

Per `01_business_context/LEGAL_DISCLAIMER.md`. Every message must comply with these rules:

**Allowed:**
- "מומחים שלנו מטפלים בערעור"
- "אנחנו עוזרים לך לנסח ולהגיש"
- "המון דוחות מתבטלים בגלל..."
- "צוות מומחים משפטיים" (in the specific "are you a law firm" answer)

**Forbidden:**
- "עורכי הדין שלנו" / "עו"ד שלנו" (as a general reference — "צוות מומחים" instead)
- "אנחנו מבטיחים ביטול"
- "אנחנו מגישים בשמך" (the user signs and submits — even on VIP)
- Any specific cancellation-rate claim without data ("85% מהדוחות מתבטלים" → no)

**Gray area handle-with-care:**
- "נלחם בשבילך" / "נילחם עליך" — OK as long as the underlying mechanism (drafting, not representation) is clear elsewhere
- "הפניה לעו"ד" — fine, it's referral not representation

---

## 0.12 Escalation triggers — bot hands off to human

Per `06_bot/knowledge_base/escalation_rules.md`. The bot **must** escalate (sets status to `escalated`, sends canonical handoff message, pages the human team) on any of:

1. Explicit human request ("רוצה לדבר עם בן אדם", "תעבירו אותי לנציג")
2. Legal threat against Road Protect ("תביעה", "עו"ד שלי", "תלונה")
3. Refund / dispute on a paid case
4. Mention of death, bereavement, serious illness
5. Complaint about the bot's behavior specifically
6. Mental-health distress signal
7. Same intent misunderstood by bot 2 turns in a row
8. Question about an active appeal in progress (status check)

After escalation, **all outbound sequences for the user are paused** until the human resolves. Resumes only on explicit `human_resolved` event with `resume = TRUE` flag.

---

## 0.13 Variables (templated tokens)

Every scenario uses a subset of these. Vendor must wire them to the source-of-truth data system.

| Token | Source | Fallback if missing |
|---|---|---|
| `{{name}}` | `user.first_name` from CRM | "שלום" (skip the personalized greeting) |
| `{{plate}}` | `user.vehicle.plate` | None — if missing, fine-related scenarios skip |
| `{{fines_count}}` | count of `fines` where `user_id = X AND status = 'open'` | None — fine-count scenarios skip if 0 |
| `{{fine_details}}` | structured block: violation type / amount / authority / date | None — if missing, scenario is broken; alert ops |
| `{{coupon_code}}` | always `SAVE30` — 30% off the **one-off appeal (₪49)**, C7 only. No `SAVE50`, no coupon on VIP (Yossi's decision). | Suppress C7 coupon touch |
| `{{events_count}}` | scans/fines detected during user's free year | Use copy variant without this number |
| `{{plan_link}}` | https://roadprotect.co.il/plans (UTM tagged per scenario) | None — required, alert ops |
| `{{appeal_link}}` | link back into the single-fine appeal flow (₪49) | None — required for C7 |
| `{{appeals_link}}` | WhatsApp link to the appeals department (052-586-6982) | None — required for appeal routing in B1/C1 |

**UTM tagging**: every `{{plan_link}}` includes `?utm_source=whatsapp&utm_medium=bot&utm_campaign=<scenario_code>&utm_content=<touch_n>&utm_term=<variant>`. The dashboard joins on these to attribute conversion.

---

## 0.14 Quality bar — every message must pass these checks

Inline at the bottom of every scenario file. Apply before declaring a touch ready:

- [ ] Opens with `היי {{name}}` (or fallback `שלום`) when name is available
- [ ] Identifies brand (Road Protect / כאן Road Protect) within first paragraph
- [ ] States the *reason* for reaching out in 1 clear sentence
- [ ] Provides value or context before any CTA
- [ ] Ends with one clear next step (a question or a CTA)
- [ ] Discloses AI identity if cold (C1, C3 touch 1)
- [ ] ≤ 2 emojis; 🛡️ is the brand default
- [ ] No legal-line violations (see § 0.11)
- [ ] ≤ 6 short paragraphs; split if longer
- [ ] Gender-neutral in touch 1; gendered after detection
- [ ] No invented stats / SLAs
- [ ] Variables resolve cleanly with fallbacks

---

## 0.15 Event emission summary — what gets logged

Every touch and every state transition emits one event. Canonical events (full schema in `dashboard-spec/02_event_schema.md`):

| Event | Fired when |
|---|---|
| `scenario.eligible` | User enters `eligible` |
| `scenario.suppressed` | Eligible but blocked by suppression matrix |
| `touch.sent` | Outbound message dispatched to WhatsApp |
| `touch.delivered` | WhatsApp delivery receipt |
| `touch.read` | WhatsApp read receipt (if API supports) |
| `touch.replied` | User replied to this specific touch |
| `branch.taken` | A reply was classified into branch B1/B2/B3/... |
| `objection.raised` | Reply matched an objection category (price, time, distrust, etc.) |
| `escalated` | Bot handed off |
| `converted` | User performed scenario success action |
| `opted_out` | User triggered opt-out |
| `sequence.exhausted` | All planned touches sent, no reply |
| `sequence.expired` | Trigger window passed |
| `bad_feedback` | User signaled complaint / cancellation intent |

Every event carries: `user_id`, `phone`, `scenario`, `touch_n`, `variant`, `timestamp`, `payload` (event-specific fields).

---

## 0.16 Bad-feedback signal — definition

The dashboard's "bad feedback / wanted to revoke sub / who" panel is driven by this signal. A `bad_feedback` event fires when the user's reply matches **any** of:

1. **Explicit complaint phrase**: "מעצבן", "ספאם", "טרחנים", "הזיותם", "מה אתם רוצים ממני"
2. **Cancellation / refund intent**: "תבטלו לי", "תחזירו לי כסף", "אני רוצה לבטל את המנוי"
3. **Abusive language** toward bot or brand
4. **Legal threat** (also escalates per § 0.12)
5. **Sentiment classifier** scores reply < -0.6 on a -1 to +1 scale (if vendor supports — fallback to phrase-list only)

The event payload includes the user's exact reply for review. Dashboard shows it as a clickable row with the user identity revealed (name, phone, current subscription status, scenario context).

**This is *not* the same as opt-out.** Bad feedback = signal that something is off. Opt-out = explicit removal. Both can coexist.

---

## 0.17 What the vendor needs to confirm before building

Hard questions the vendor must come back with answers / decisions on. These are the "≤ 10 clarification questions" we expect — anything beyond these means the spec has gaps.

1. WhatsApp API choice — read receipts available?
2. CRM of record — where do `user`, `fine`, `subscription` tables live?
3. Sentiment classifier — built-in or external? (Affects bad-feedback detection)
4. Variable freshness SLA — how stale is `{{fines_count}}` when a touch fires?
5. A/B test infrastructure — does the vendor's platform support variant tagging in events?
6. Quiet-hours timezone — confirm Asia/Jerusalem in all environments
7. Opt-out — is there an existing master opt-out table to write back to?
8. Coupon generation — single shared code per discount tier, or per-user unique codes?
9. UTM-to-conversion join — what's the path from `utm_campaign=C5&utm_content=touch_1` on a checkout to a tracked `converted` event?
10. Escalation endpoint — Slack? Shared inbox? Phone call?
