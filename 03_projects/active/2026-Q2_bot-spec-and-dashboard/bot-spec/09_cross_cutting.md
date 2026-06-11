# 09 — Cross-Cutting Spec

*Rules that apply to **every** scenario. If a scenario file is silent on one of these topics, the rule here governs.*

This doc consolidates and expands on `00_overview.md` for vendor convenience — it's the rule reference vendor will pin to their monitor.

---

## 9.1 Conversation state machine — extended

Beyond the per-scenario states in `00_overview.md` § 0.2, every user has a global session state:

| Session state | Meaning |
|---|---|
| `idle` | No active conversation. Outbound scenarios may fire. |
| `c2b_active` | User is in an outbound sequence (any C scenario). |
| `b1_active` | User is in an inbound session (within 12h of last message). |
| `b1_active + c2b_active` | User started an inbound while mid-outbound. B1 takes priority for *responding*; C2B sequence touches are suppressed until B1 session ends. |
| `escalated` | Human is handling. All outbound suspended. |
| `opted_out` | All outbound permanently disabled (until re-opt-in). |

**Transitions** emit `session.state_changed` events for the dashboard.

---

## 9.2 Variable resolution and fallbacks

When a touch is about to send, the orchestrator resolves variables. If any required variable can't resolve:

| Variable | Required? | Fallback behavior |
|---|---|---|
| `{{name}}` | No | Replace with `שלום` (skip personalization) |
| `{{plate}}` | Required for fine-related scenarios | Skip the touch, log `variable_resolution_failed`, alert ops |
| `{{fine.*}}` | Required for C5/C7 | Skip the touch, alert ops |
| `{{fines_count}}` | Required for C2/C3/C6_had_fines | If 0, route to no-fines variant; if null, skip |
| `{{coupon_code}}` | Required for C7 touch 2+, C3 touch 3, C6 touch 4 | Skip the touch (don't send coupon-less version) |
| `{{plan_link}}` | Required (all scenarios) | Critical alert — never silently drop, escalate to ops |

**Rule**: don't send a message with a visible `{{token}}` in it. Ever. If resolution fails and fallback is "skip touch," it's better to skip than to send broken copy.

---

## 9.3 Frequency caps (consolidated from § 0.6)

Per user, rolling windows:

- **1 outbound message per 24h**
- **3 outbound messages per 7 days**
- **8 outbound messages per 30 days**

**Inbound responses do not count** toward outbound caps. If the user is talking, we talk back.

**Cap-deferred touches**: when a touch hits a cap, defer until window opens. If deferral pushes past the scenario's `expires_at`, mark `expired`.

**Override**: C5 (real-time fine alert) **can override the 24h cap** if the previous outbound was a low-stakes touch (C1, C4 month-1, C6). It does **not** override the 7-day or 30-day caps. If those are hit, defer per usual.

---

## 9.4 Quiet hours (consolidated from § 0.7)

| Window | No outbound |
|---|---|
| Weekday nights | 22:00 → 08:00 Asia/Jerusalem |
| Shabbat | Friday 17:00 → Saturday 21:00 Asia/Jerusalem |
| Yom Kippur | All day, 0:00 → 24:00 |
| Rosh Hashanah | Day 1, 0:00 → 24:00 |
| Pesach | Erev + Day 1, 0:00 → 24:00 (each) |
| Sukkot | Day 1, 0:00 → 24:00 |
| Shavuot | Day-of, 0:00 → 24:00 |
| Yom HaAtzmaut | All day |
| Yom HaZikaron | All day |

**Holiday calendar**: vendor maintains list of dates per Hebrew calendar. **2026 dates** (relevant for v1 launch):

- Yom HaZikaron: 2026-04-22
- Yom HaAtzmaut: 2026-04-23
- Shavuot: 2026-05-22
- Rosh Hashanah: 2026-09-12 (day 1)
- Yom Kippur: 2026-09-21
- Sukkot: 2026-09-26 (day 1)
- Pesach 2027 — vendor responsible for adding when calendar rolls

**Inbound responses**: always answered, including in quiet windows. Quiet hours apply to outbound only.

---

## 9.5 Opt-out — full spec (extends § 0.8)

**Detection mechanism**: case-insensitive partial match on any inbound message (B1 or response to C2B).

**Trigger phrase list** (additive, vendor can extend):

Hebrew:
- "הסר אותי", "להסיר", "תסיר", "תסירו"
- "לא לפנות שוב", "אל תפנו", "אל תפנה", "אל תתקשרו"
- "להפסיק לקבל הודעות", "להפסיק"
- "להוריד מהרשימה", "להוריד אותי"
- "די", "מספיק" — **only if** preceded by a complaint signal (not as standalone — "די יקר" is not opt-out)
- "ביטול תפוצה"

English (rare but possible):
- "stop", "unsubscribe", "remove me"

**Edge cases — NOT opt-out**:
- "לא עכשיו" / "לא בטוח" / "אולי בעתיד" — hesitation, sequence continues per branch
- "די יקר" / "מספיק כסף" — complaint about price, route to price objection
- "לא רוצה את זה" — declined but not opted out (next scenario can still fire eventually)

**Bot response to opt-out trigger**: canonical message per § 0.8 step 3.

**Permanence**: opt-out is **permanent** until user explicitly messages in and confirms re-opt-in (per B1 re-onboarding flow).

**Granularity**: opt-out is **global** — applies to all C2B scenarios. B1 inbound responses still work (because user initiated).

---

## 9.6 Gender detection — full spec (extends § 0.9)

**Default**: gender-neutral verb forms in touch 1 of every scenario.

**Detection trigger**: user's first reply.

**Lock rules**:

| Cue in reply | Lock |
|---|---|
| Masculine 1st-person verb: "מעוניין", "אני יודע", "אני רוצה" | Masculine |
| Masculine adjective: "סגור", "מוכן", "ברור לי" | Masculine (with caveat — these are also used by women in informal speech; weight is lower) |
| Feminine 1st-person verb: "מעוניינת", "אני יודעת", "אני רוצה" + feminine adjective | Feminine |
| Feminine adjective: "סגורה", "מוכנה", "ברור לי" + feminine context | Feminine |
| Name-based lookup (for known names like יוסי / רחל) | Use as secondary signal, not primary |
| Ambiguous reply ("כן", "תשלח לי", "מעניין") | Stay neutral |

**Once locked, stay locked** for the rest of the user's lifetime conversation (not just session). Stored in user record.

**Re-evaluation**: if a locked masculine user replies with strongly feminine cues later → flag for review. Don't silently flip. (May indicate the original account holder isn't the one messaging now.)

**Forbidden in warm/emotional copy**: slash-forms like "מעוניין/ת", "סגור/ה". They kill the empathy register. Write separate masculine + feminine variants instead.

**Permitted in functional/transactional copy**: slash-forms acceptable in (e.g.) coupon redemption instructions where empathy isn't required.

---

## 9.7 AI disclosure — when, how, what (extends § 0.10)

**Mandatory disclosure moments**:

1. **First message of a cold-list scenario** (C1, C3) — include "אני סוכן AI דיגיטלי" in touch 1.
2. **First B1 message** — include "אני סוכן AI דיגיטלי" or "אני העוזר הדיגיטלי של Road Protect" in opener.
3. **When user asks directly** — "מי אתה?", "אתה בנאדם?", "אתה אמיתי?", "בוט?" → respond truthfully.
4. **After 5+ turns with no prior disclosure** — opportunistically disclose on a natural beat.

**Forbidden language**:
- ❌ "אני [human name]" (no human persona)
- ❌ "אני עובדת ב-Road Protect" (implies human employee)
- ❌ Saying yes to "אתה בנאדם?" — that's a lie

**Approved disclosure phrasings**:
- ✅ "אני סוכן AI דיגיטלי"
- ✅ "אני העוזר הדיגיטלי של Road Protect"
- ✅ "אני בוט / סוכן חכם של Road Protect"

---

## 9.8 Legal-line discipline (extends § 0.11)

**The non-negotiable lines** (from `01_business_context/LEGAL_DISCLAIMER.md`):

| Allowed | Forbidden |
|---|---|
| "המומחים שלנו מנסחים את הערעור" | "עורכי הדין שלנו מייצגים אותך" |
| "אנחנו עוזרים לך לערער" | "אנחנו מייצגים אותך מול הרשויות" |
| "המון דוחות מתבטלים בגלל..." | "85% מהדוחות מתבטלים" (without published data) |
| "צוות מומחים משפטיים" (in specific "are you a law firm?" answer only) | "Road Protect הוא משרד עורכי דין" |
| "נלחם בשבילך" (when context clarifies mechanism) | "מבטיחים ביטול" |
| "הפניה לעו"ד מומחה" (referral only) | "עו"ד שלנו עוזר לך" (as general reference) |

**Pre-deploy review**: every new message variant added in v1.1+ must be reviewed against this table.

**Auto-detection** (if vendor can): pattern-match the message against forbidden phrases before sending. Block if hit.

---

## 9.9 Escalation triggers — full table (extends § 0.12)

| Trigger | Sub-cause | Always escalate? | Suggested urgency |
|---|---|---|---|
| Explicit human request | "נציג", "בן אדם", etc. | Yes | Medium |
| Legal threat | "תביעה", "עו"ד שלי", "תלונה" | Yes | High |
| Refund / dispute | "תחזירו לי", "תבטלו את החיוב" | Yes | High |
| Death / serious illness | Bereavement, hospitalization mentions | Yes | High |
| Bot complaint | "הסוכן שיקר", "הציק לי" | Yes | High |
| Mental-health distress | Self-harm, severe financial crisis | Yes | Highest (page on-call) |
| Account question (non-self-serve) | Cancellation, billing dispute | Yes | Medium |
| Appeal status (VIP) | "מה קורה עם הערעור" | Yes | Medium |
| Repeated misunderstanding | 2+ turns without progress | Yes after 2 | Low |
| Technical issue (specific to user) | "המערכת לא עובדת אצלי" | After 1 attempt | Medium |
| General confusion | Bot can attempt 2 clarifications | After 2 attempts | Low |

**Handoff payload**: when escalating, the orchestrator sends to the human channel (Slack / shared inbox) a structured packet:

```json
{
  "user_id": "...",
  "phone": "...",
  "scenario": "C5",
  "reason": "legal_threat",
  "urgency": "high",
  "last_5_messages": [...],
  "suggested_first_response": "...",
  "user_subscription": "vip",
  "user_lifetime_revenue_ils": 489
}
```

**SLA targets** (per `escalation_rules.md`):
- Mental-health flag: < 30 min, all hours
- Legal threat: < 30 min, business hours
- Refund / dispute: < 2 business hours
- Appeal status: < 4 business hours
- Generic human request: < 1 business day

---

## 9.10 Suppression matrix — full version (extends § 0.5)

When multiple scenarios are eligible for the same user at the same time:

| User state | Eligible scenarios | Winner | Why |
|---|---|---|---|
| Fresh fine just detected | C5 + (any other) | **C5** | Real-time / user-friction |
| Lapsed + new fine | C3 + C5 | **C5** | Fresh fine moment is hotter |
| In-app fine view, no checkout, free user | C5 + C7-B | **C5** | C5 has higher conversion intent |
| In-app fine view, no checkout, VIP user | None | N/A | VIP doesn't need C7 — appeal is auto-handled |
| 30 days from expiry + has fine detected | C5 + C6 | **C5** | Fresh fine > pre-expiry |
| 14 days from expiry + view fine in app | C7-B + C6 | **C7-B** | Coupon path has higher close rate |
| 30 days from expiry + nothing else | C6 only | C6 | |
| Cold lead + signs of life (e.g. opened previous link) | C1 | C1 | |
| Trademobile-active + fines | C2 + C5 if fine fresh | **C5** if fresh, **C2** if old | |
| Just-purchased Trademobile (within 7 days) | C4 + C1 | **C4** | Onboarding owns first 30 days |

**General rule**: time-sensitive scenarios beat calendar-driven scenarios; conversion-likely scenarios beat education scenarios.

---

## 9.11 Conversation timeout

- **C2B sequence touch timer**: between touches in a sequence, the gap is per-scenario (typically 72h–7d). The whole sequence is `exhausted` after the last planned touch + 24h grace.
- **B1 session timeout**: 12 hours after last message. New inbound after timeout = new B1 session.
- **Escalation timeout**: if human doesn't respond within SLA, the escalation event is re-flagged and the orchestrator sends a reminder ping to the human channel.

---

## 9.12 What every C2B scenario file must contain (vendor compliance checklist)

Use this as the spec-completeness audit:

- [ ] Critique of current version (for context)
- [ ] Trigger predicate (machine-readable)
- [ ] Variables used + sources + fallbacks
- [ ] Sequence with N touches (each: delay, variants, skip conditions, exit conditions, events emitted)
- [ ] Quality checklist per touch
- [ ] Branches (when user replies)
- [ ] Suppression and exit rules (or reference to § 9.10)
- [ ] Events emitted (with payload notes)
- [ ] A/B testing slots
- [ ] Open questions for Yossi

A scenario file missing any of these is **not vendor-ready**.

---

## 9.13 What B1 inbound file must contain

- [ ] Trigger
- [ ] Intent taxonomy (all 9 v1 intents)
- [ ] Classification mechanism
- [ ] Opening message
- [ ] Per-intent sub-flows
- [ ] Re-onboarding for opt-out
- [ ] Cross-scenario coordination
- [ ] Events emitted

---

## 9.14 Things the bot must NEVER do (consolidation)

1. Claim lawyer representation
2. Guarantee fine cancellation
3. Use a human persona name
4. Send a message during quiet hours (except inbound responses)
5. Exceed frequency caps
6. Ignore opt-out
7. Display unresolved `{{tokens}}`
8. Send coupons outside the explicit C3/C6/C7 contexts
9. Quote invented statistics or SLAs
10. Open a cold-list message without AI disclosure
11. Use slash-form gender ("מעוניין/ת") in warm copy
12. Mock or argue with a user expressing frustration
13. Send a message in a language the user didn't use (translate, don't switch)
14. Push a CTA before identifying their intent (in B1) or context (in C2B)

---

## 9.15 Vendor onboarding doc — quick-start

When vendor joins, they read in this order:

1. `00_overview.md` (framework)
2. This file (`09_cross_cutting.md` — the rule reference)
3. `01_c1_cold_outreach.md` (the reference scenario; format every scenario follows)
4. The other scenario files in order
5. `dashboard-spec/*` for event schema + funnel definitions

Estimated time-to-build-readiness: **2 working days of reading + clarifying questions**.
