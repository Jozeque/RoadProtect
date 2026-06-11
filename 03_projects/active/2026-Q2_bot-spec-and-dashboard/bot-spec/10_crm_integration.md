# 10 — CRM Integration & Lead Warmth Model

*The bot reads from and writes to the Road Protect CRM. This doc is the contract.*

**Audience**: the new vendor — must read this before mapping any trigger predicate or implementing any branch logic.

The CRM is the **source of truth** for who the user is, what we know about them, and what state they're in. Every trigger predicate in `01_c1_*` through `08_b1_*` is shorthand for "read these CRM columns and evaluate." This doc resolves the shorthand.

---

## 10.1 CRM table — column inventory

The user-row table in the CRM has **19 columns**. Listed in the order they appear in the UI (RTL), with type, source (manual / system / AI-computed), and the bot's relationship to each (Read = bot uses it, Write = bot updates it).

| # | Column (Hebrew) | English gloss | Type | Source | Bot R/W |
|---|---|---|---|---|---|
| 1 | שם | Name | string | manual / signup | R |
| 2 | אימייל | Email | string | manual / signup | R |
| 3 | טלפון | Phone | E.164 string | manual / signup | R (primary identity for WhatsApp) |
| 4 | מקור הגעה | Acquisition source | **enum** (§10.2) | manual / partner sync | R |
| 5 | ערך לקוח | Customer value (LTV) | numeric (₪) | system aggregate | R (drives high-LTV branches) |
| 6 | מנוי נוכחי | Current subscription | **enum** (§10.2) | billing system | R (drives most triggers) |
| 7 | קנסות פעילים | Active fines (count) | integer | fine-detection system | R (drives C2/C3/C5/C7 segmentation) |
| 8 | ערעורים | Appeals (count) | integer | appeal system | R |
| 9 | ימים לא פעיל | Days inactive | integer | system computed | R (decays warmth) |
| 10 | סנטימנט AI | AI sentiment | enum: 🟢 חיובי / 🟡 ניטרלי / 🔴 שלילי | bot writes | **R + W** |
| 11 | סיכון נטישה | Churn risk | enum: נמוך / בינוני / גבוה | computed | R (suppresses pushy scenarios) |
| 12 | סטטוס ערעור אחרון | Last appeal status | **enum** (§10.2) | appeal system | R |
| 13 | תאריך חידוש / סיום | Renewal / end date | date | billing system | R (drives C6) |
| 14 | יחס קנסות | Fine ratio | numeric (cancelled / total %) | computed | R |
| 15 | קנסות שאותרו (Fleet) | Detected fines — Fleet | integer | fine-detection (Fleet-cohort only) | R |
| 16 | פעילות AI אחרונה | Last AI activity | timestamp | bot writes | **R + W** |
| 17 | תקשורת אחרונה | Last communication | timestamp | any outbound system | R (drives frequency caps) |
| 18 | תאריך הצטרפות | Join date | date | signup | R |
| 19 | פעולות | Actions | UI-only | — | — |

**Two columns the bot WRITES to**: `סנטימנט AI` (column 10) and `פעילות AI אחרונה` (column 16). Everything else is read-only from the bot's perspective. Write contract is in §10.5.

---

## 10.2 Enum values (the 3 dropdowns shown in CRM UI)

These are the exact strings the CRM stores. Any trigger predicate referencing these fields must use these exact values.

### `מקור הגעה` (Acquisition source)

| CRM value | Maps to bot-spec concept |
|---|---|
| `אורגני/פרטי` | Cold-organic / direct landing-page conversion |
| `ממומן` | Paid-acquisition (ads, sponsored content) |
| `טריידמוביל B2B` | Trademobile partner cohort (P1, P4 personas) |
| `פנגו B2B` | Pango partner cohort |
| `לא ידוע` | Source unrecorded (legacy or imported leads) |

**Implication for scenarios:**

- C4 (Trademobile welcome) fires only on `מקור הגעה = "טריידמוביל B2B"`
- C1 (cold outreach) fires on `אורגני/פרטי` OR `ממומן` OR `לא ידוע` — never on B2B sources (those have their own onboarding)
- Pango B2B has no dedicated scenario yet — flag for v2

### `מנוי נוכחי` (Current subscription)

| CRM value | Maps to bot-spec concept |
|---|---|
| `מנוי בתשלום` | Paying customer — Detection (₪99/yr) OR VIP (₪489/yr). **Note**: CRM does not distinguish tiers here → see §10.3 open question. |
| `מנוי חינם` | Free tier (no payment) — likely a legacy / promo free plan. **Ambiguous** — see §10.3. |
| `ערעור חד-פעמי` | Paid one-off (₪49) for a single appeal. Not a subscription. |
| `Trial (Trademobile)` | Trademobile free year. The bot's `trademobile_free` state. |
| `ללא מנוי` | No active subscription. Includes BOTH never-subscribed leads AND lapsed users — disambiguate with `תאריך חידוש / סיום`. |

**Critical disambiguation rule** for `ללא מנוי`:

```
IF (תאריך חידוש / סיום IS NULL)
  → user is a "lead" (never subscribed)         → C1 eligible
IF (תאריך חידוש / סיום < NOW())
  → user is "lapsed"                            → C3 eligible
IF (תאריך חידוש / סיום > NOW() AND מנוי = "ללא מנוי")
  → data inconsistency                          → log + skip
```

### `סטטוס ערעור אחרון` (Last appeal status)

These are the stages of an appeal's lifecycle. The bot uses this to know what stage the user's most recent appeal is in.

| CRM value | Meaning | Bot behavior implication |
|---|---|---|
| `חדש` | Appeal opened, no data entered yet | Bot can prompt for fine details (B1 I1 routing) |
| `פרטים בסיסיים` | User provided name + plate | Bot can prompt for violation details |
| `פרטי עבירה` | Violation details collected | Appeal is being drafted by experts — bot does NOT prompt, escalates status questions |
| `הוגש` | Appeal submitted by user to authority | Bot acknowledges, does not solicit more info |
| `נשלח לרשות` | System dispatched to authority | Same — passive monitoring |
| `נדחה` | Authority rejected | High-touch moment: bot should NOT push upsell; route to human empathy |
| `אושר` | Authority accepted, fine cancelled | Celebration moment — opportunity for VIP cross-sell if not already VIP, and for "tell a friend" referral |
| `טופל` | Closed-out (paid, withdrawn, or other resolution) | Neutral close. Eligible for next-cycle scenarios. |

**Suppression rule**: if `סטטוס ערעור אחרון ∈ {פרטי עבירה, הוגש, נשלח לרשות}` for a user — **no C2B outbound** about that specific fine. The expert team owns the conversation. Bot can still respond to inbound (B1).

---

## 10.3 Field mapping — every bot-spec variable to its CRM column

Cross-reference for the vendor. Left column = what's used in `01_c1_*` through `08_b1_*`. Right column = the actual CRM source.

| Bot-spec variable / predicate | CRM column / derivation |
|---|---|
| `user.first_name` | `שם` (split on first space) |
| `user.email` | `אימייל` |
| `user.phone` | `טלפון` |
| `user.subscription` | `מנוי נוכחי` — but see §10.3.1 for tier-resolution |
| `user.acquisition_source` | `מקור הגעה` |
| `user.subscription.expires_at` | `תאריך חידוש / סיום` |
| `user.subscription.started_at` | `תאריך הצטרפות` (proxy — assumes join = first sub start) |
| `user.subscription.auto_renew` | NOT in CRM today — **gap**, see §10.7 |
| `user.lifetime_revenue_ils` | `ערך לקוח` |
| `user.ltv_score` | derive: `ערך לקוח > 500 → high` (see §10.4 warmth scoring) |
| `user.opted_out` | derive: `סנטימנט AI = שלילי` AND last_communication contains opt-out trigger phrase. Maintained separately in vendor stack. **Gap** — needs dedicated CRM field, see §10.7 |
| `fines.open_count_for_user` | `קנסות פעילים` |
| `fines.detected_count_total` | needs join — currently aggregated in `קנסות שאותרו (Fleet)` for Fleet cohort only |
| `fines.cancellation_ratio` | `יחס קנסות` |
| `fine.detected_at` (real-time C5) | NOT in CRM row — comes from fine-detection event stream. CRM `קנסות פעילים` is a counter only. |
| `user.last_outbound_at` | `תקשורת אחרונה` |
| `user.last_bot_interaction_at` | `פעילות AI אחרונה` |
| `user.days_inactive` | `ימים לא פעיל` (already computed) |
| `user.sentiment` | `סנטימנט AI` — see §10.5 for the bot's write contract |
| `user.churn_risk` | `סיכון נטישה` |
| `user.appeal_state` | `סטטוס ערעור אחרון` |

### 10.3.1 Tier resolution for `מנוי בתשלום`

The CRM stores `מנוי בתשלום` without distinguishing Detection (₪99) from VIP (₪489). The bot needs to know which tier. Two ways:

1. **Preferred** — CRM adds a `מסלול` (plan tier) column with values `איתור / VIP / ערעור-נקודתי` for paying customers.
2. **Fallback** — vendor joins on the billing system's plan field, separately from the user row.

Until #1 ships, **scenarios that depend on the Detection vs VIP distinction must read from the billing-system join**. List of affected scenarios: C2, C5, C6, C7 (all of which gate on "not already VIP").

---

## 10.4 Lead-warmth scoring model

The user said these fields are how we know "רמת החמימות של הליד ואיך לנהל ולנתב את השיחה" — lead warmth and routing. Spec for how the bot derives warmth from CRM fields:

### Warmth score (0–100)

Compute from CRM columns at the moment the bot evaluates a trigger:

```
score = 0

// Base score from subscription state
IF מנוי נוכחי = "מנוי בתשלום"        →  score += 60
IF מנוי נוכחי = "Trial (Trademobile)" →  score += 50
IF מנוי נוכחי = "מנוי חינם"           →  score += 40
IF מנוי נוכחי = "ערעור חד-פעמי"      →  score += 35
IF מנוי נוכחי = "ללא מנוי" AND has end_date    →  score += 25  // lapsed
IF מנוי נוכחי = "ללא מנוי" AND no end_date     →  score += 5   // cold lead

// Active pain
IF קנסות פעילים >= 1                  →  score += 15
IF קנסות פעילים >= 3                  →  score += 10  // additive — stacks on top of +15

// Recent engagement
IF ימים לא פעיל <= 7                  →  score += 10
ELSE IF ימים לא פעיל <= 30            →  score += 5
ELSE IF ימים לא פעיל >= 180           →  score -= 15

// Sentiment
IF סנטימנט AI = חיובי                 →  score += 10
IF סנטימנט AI = שלילי                 →  score -= 25  // strong penalty

// Churn risk
IF סיכון נטישה = גבוה                 →  score -= 15
IF סיכון נטישה = נמוך                 →  score += 5

// Past appeal outcomes
IF סטטוס ערעור אחרון = אושר            →  score += 15  // happy customer
IF סטטוס ערעור אחרון = נדחה            →  score -= 10  // wound recently

// LTV
IF ערך לקוח >= 1000 (₪)                →  score += 10
IF ערך לקוח >= 500                     →  score += 5

// Clamp
score = max(0, min(100, score))
```

### Warmth buckets

| Score | Bucket | Bot behavior |
|---|---|---|
| 75–100 | 🔥 **Hot** | High-intent. Push closer faster (skip soft-diagnostic, surface CTA earlier). Eligible for upsell scenarios. |
| 50–74 | ☀️ **Warm** | Standard flow. Diagnostic-first per spec. |
| 25–49 | 🌤️ **Lukewarm** | Slower cadence — extend touch-2/touch-3 delays. Stay informative, deflect coupons unless approved. |
| 0–24 | ❄️ **Cold** | Single-touch only. No coupons. Light reactivation OR full re-introduction (C1-style). |

### Routing decisions driven by warmth

| Decision | Rule |
|---|---|
| **Which scenario fires** | Hot users → high-priority scenarios (C5/C7). Cold users → C1 or skip. |
| **Coupon eligibility** | The only coupon is `SAVE30` (30% off the ₪49 appeal), issued in **C7 only** (appeal-abandoners). C3/C6 issue no coupons; VIP is never discounted. **No coupons to cold users.** |
| **Touch cadence** | Hot: spec defaults. Lukewarm: +2 days on each delay. Cold: skip touch 2 and touch 3 entirely (one shot only). |
| **Empathy intensity** | Hot users tolerate direct CTAs. Cold + low sentiment → soften opener, lead with question. |
| **Real-time fire (C5)** | Always fires regardless of warmth — fresh fine overrides warmth gating. But the *copy* used is warmth-adjusted (cold user gets less urgent framing). |
| **Suppression** | Warmth ≤ 24 + `סנטימנט AI = שלילי` + `סיכון נטישה = גבוה` → **suppress all outbound for 30 days**. Don't make a bad situation worse. |

---

## 10.5 Bot write-back contract

The bot writes to two CRM columns. Spec:

### 10.5.1 `סנטימנט AI` write rule

On every user reply the bot receives, compute sentiment from the reply text and update the column. Rules:

| Bot-detected signal in reply | New sentiment value | Override behavior |
|---|---|---|
| Compliment / thanks / "תודה רבה" / explicit positive | 🟢 חיובי | Overrides existing UNLESS current value is 🔴 שלילי (don't whiplash) |
| Neutral information / questions / "אוקיי" / "תשלח לי" | 🟡 ניטרלי | Only updates if current is null |
| `bad_feedback` event fires (per `00_overview.md` § 0.16) | 🔴 שלילי | **Always overrides** — bad feedback is sticky |
| Opt-out trigger | 🔴 שלילי | Same as bad_feedback |
| Multiple turns of frustration in a single session | 🔴 שלילי | After 2nd frustration cue in a session |

**Sticky negative window**: once `סנטימנט AI = שלילי` is set, it requires a *deliberate* positive event (compliment, conversion, successful appeal closure) to upgrade back to neutral/positive. Don't let a passive "תודה" auto-clear a previous negative.

### 10.5.2 `פעילות AI אחרונה` write rule

Updated on every `touch.sent`, every `touch.replied`, and every `escalated` event. The timestamp is the most recent of:
- Last outbound touch dispatched
- Last user reply received
- Last escalation
- Last inbound B1 message answered

This column powers `ימים לא פעיל` computation and the frequency-cap logic.

---

## 10.6 Read freshness — what the bot can assume

When the bot reads CRM data at trigger-evaluation time, freshness guarantees:

| Column | Required freshness | Reasoning |
|---|---|---|
| `מנוי נוכחי` | ≤ 15 minutes | A user who converted 20 min ago must not be pitched again |
| `קנסות פעילים` | ≤ 5 minutes | C5 is real-time — needs fresh fine data |
| `תאריך חידוש / סיום` | ≤ 1 hour | Drives C6 timing; daily resolution is enough but hourly is safer |
| `סנטימנט AI`, `סיכון נטישה` | ≤ 30 minutes | Affects suppression — stale data could push to a hostile user |
| `סטטוס ערעור אחרון` | ≤ 15 minutes | Critical for suppression — don't pester a user mid-appeal |
| `תקשורת אחרונה` | ≤ 5 minutes | Frequency cap depends on this |
| `ערך לקוח` | ≤ 24 hours | Aggregate metric — slower updates acceptable |

If any required-freshness window is breached at evaluation time, the orchestrator should defer the touch and re-evaluate when data refreshes. Better to send a touch 30 min late than to send it to the wrong user state.

---

## 10.7 Gaps — fields the CRM doesn't have today

These are gaps the vendor should flag during onboarding. The spec needs them; the current CRM screenshot doesn't show them.

| Missing field | Why needed | Suggested resolution |
|---|---|---|
| `מסלול` (Detection vs VIP within paid sub) | Multiple scenarios gate on this | Add column OR expose via billing-system join |
| `opt_out_flag` (explicit, boolean) | Currently inferred — bot needs a deterministic field | Add `הוסר_מתפוצה` boolean column |
| `auto_renew_flag` | C6 trigger reads this | Add column |
| `subscription_history` (array) | C3 needs prior-status; "lapsed" needs to know what they were lapsed from | Either a sub-table or last_known_plan column |
| `fine_detection_event_stream` access | C5 fires on fresh-fine events, not on count-changes | Vendor needs read access to the event stream, not just CRM |
| `correlation_id` per conversation | The event schema requires this (`dashboard-spec/02_event_schema.md`) | Vendor maintains in their own state; doesn't need to be in CRM |

---

## 10.8 How each scenario reads the CRM — revised triggers

Quick reference. The full predicates in scenarios `01_*` through `07_*` are restated here in CRM-native terms.

### C1 — Cold Outreach
```
מנוי נוכחי = "ללא מנוי"
AND תאריך חידוש / סיום IS NULL                    -- never subscribed
AND תאריך הצטרפות BETWEEN (NOW() - 2 years) AND (NOW() - 60 days)
AND תקשורת אחרונה IS NULL OR <= (NOW() - 180 days)
AND סנטימנט AI != "שלילי"
AND warmth_score < 50                              -- only true cold qualifies
AND מקור הגעה IN ("אורגני/פרטי", "ממומן", "לא ידוע")
```

### C2 — Trademobile Active w/ Fines
```
מנוי נוכחי = "Trial (Trademobile)"
AND תאריך הצטרפות <= (NOW() - 14 days)
AND תאריך חידוש / סיום > (NOW() + 60 days)
AND קנסות פעילים >= 1
AND סטטוס ערעור אחרון NOT IN ("פרטי עבירה", "הוגש", "נשלח לרשות")
```

### C3 — Past Customer Winback
```
מנוי נוכחי = "ללא מנוי"
AND תאריך חידוש / סיום < NOW()
AND תאריך חידוש / סיום >= (NOW() - 2 years)
AND קנסות פעילים >= 1
AND warmth_score >= 25
```

### C4 — Trademobile Welcome
```
מקור הגעה = "טריידמוביל B2B"
AND מנוי נוכחי = "Trial (Trademobile)"
AND תאריך הצטרפות >= (NOW() - 2 hours)
AND no prior C4 fired for this user
```

### C5 — Free User Got Fine
Predicate stays event-driven (fires on fresh-fine event). CRM read is for context:
```
מנוי נוכחי IN ("Trial (Trademobile)", "מנוי בתשלום-איתור", "מנוי חינם")
AND warmth-bucket determines copy variant register (cold → softer; hot → direct)
```

### C6 — Pre-Expiry Retention
```
מנוי נוכחי IN ("Trial (Trademobile)", "מנוי בתשלום")
AND תאריך חידוש / סיום BETWEEN NOW() AND (NOW() + 30 days)
AND auto_renew = FALSE       -- needs gap-filled
```

### C7 — Dirty Quick Winback
Two paths per `07_c7_*.md`. CRM reads:
```
PATH A (post-C5 abandon):
  user had a C5 sequence end in exhausted/declined
  AND קנסות פעילים >= 1
  AND מנוי נוכחי != "מנוי בתשלום-VIP"
  AND warmth_score >= 35

PATH B (app fine-view, no checkout):
  app event ('fine_detail_viewed') exists
  AND no checkout in last 2h
  AND מנוי נוכחי IN ("Trial (Trademobile)", "מנוי חינם", "ללא מנוי")
  AND warmth_score >= 35
```

---

## 10.9 The CRM screen — what the operator sees

When Yossi or a support agent opens the CRM, each user row shows the 19 columns + 3 filterable dropdowns (`מקור הגעה`, `מנוי נוכחי`, `סטטוס ערעור אחרון`). The bot does not have a UI — it consumes the data through API.

**Operator actions** in the `פעולות` column (column 19) — not in scope for the bot, but worth knowing:
- Send manual outbound (overrides bot suppression — flagged in event log)
- View conversation transcript
- Force opt-out
- Refund / cancel subscription
- Open appeal

When an operator takes a manual action, the bot's pending sequence for that user **pauses for 24 hours** (gives the human action time to land), then re-evaluates.

---

## 10.10 Open questions

Hard questions the vendor must answer with us before building. These join the master list in `00_overview.md` § 0.17.

1. **`מנוי חינם` vs `Trial (Trademobile)`** — what's the difference? Is `מנוי חינם` a legacy promo tier? My current spec treats Trademobile-free as `Trial (Trademobile)` and assumes `מנוי חינם` is a separate (smaller) free tier. Confirm.
2. **`ערעור חד-פעמי` as a state** — does this column entry persist after the one-off appeal is closed, or does it revert to `ללא מנוי`? Affects re-entry logic for C1/C3.
3. **`קנסות שאותרו (Fleet)`** is Fleet-cohort-specific — is there a parallel column for non-Fleet, or is `קנסות פעילים` the catch-all?
4. **Warmth score** — should it be **computed at evaluation time** (each scenario trigger reads CRM and re-derives) or **stored as a column** (CRM recomputes daily, bot reads the stored value)? Storing is faster; computing is more accurate. Recommend storing + recomputing daily, with on-demand recompute on high-priority triggers (C5).
5. **`סטטוס ערעור אחרון` enum order** — is the dropdown's order (חדש → פרטים בסיסיים → פרטי עבירה → הוגש → נשלח לרשות → נדחה / אושר / טופל) the canonical lifecycle? Confirm — the suppression rules in §10.2 depend on this.
6. **Manual operator action propagation** — when an operator manually opts-out or refunds a user, does the CRM emit an event the bot subscribes to, or does the bot need to poll? Affects latency on suppression.
7. **Pango B2B cohort** — there's no dedicated scenario today. Should there be a `C8 — Pango B2B` (Trademobile-like welcome + activation), or do they just inherit C1/C2 paths?
8. **Sentiment field write conflicts** — if multiple systems (the bot + a human-handled chat + a support ticket) all want to write `סנטימנט AI`, who wins? Recommend: bot is the canonical writer; human-flagged sentiment overrides with `manual_override = true` flag.
