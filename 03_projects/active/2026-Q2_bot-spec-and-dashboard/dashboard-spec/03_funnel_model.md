# 03 — Funnel Model

*How the dashboard's funnel views are constructed from events.*

**Audience**: vendor (for implementation) AND Yossi (so he knows what the dashboard *can* and *cannot* tell him).

---

## The canonical C2B funnel

Every C2B scenario maps to this same funnel structure. The funnel has 8 steps; not every scenario uses every step (e.g., C4 has only 2 touches, so steps 5–6 are zero).

```
1. Eligible
   ↓ (suppression matrix may filter)
2. Reached (touch 1 delivered)
   ↓
3. Touch 1 replied
   ↓ (users who didn't reply continue to touch 2)
4. Touch 2 sent (if applicable)
   ↓
5. Touch 2 replied
   ↓
6. Touch 3 sent (if applicable)
   ↓
7. Touch 3 replied
   ↓
8. Converted
```

**Drop-off branches** (always tracked in parallel):
- → Opted out (at any step)
- → Escalated (at any step)
- → Bad feedback flagged (at any step — may or may not result in opt-out / escalation)
- → Undeliverable (at touch 1 send)
- → Expired (e.g., user paid fine externally)
- → Exhausted (sequence ended with no reply, no conversion)

---

## Funnel construction logic

For each (scenario, time_window) pair, the dashboard computes the funnel as:

```
step_1_eligible = COUNT DISTINCT user_id from `scenario.eligible` events
step_2_reached = COUNT DISTINCT user_id from `touch.delivered` WHERE touch_n=1
step_3_replied_t1 = COUNT DISTINCT user_id from `touch.replied` WHERE touch_n=1
step_4_sent_t2 = COUNT DISTINCT user_id from `touch.sent` WHERE touch_n=2
step_5_replied_t2 = COUNT DISTINCT user_id from `touch.replied` WHERE touch_n=2
step_6_sent_t3 = COUNT DISTINCT user_id from `touch.sent` WHERE touch_n=3
step_7_replied_t3 = COUNT DISTINCT user_id from `touch.replied` WHERE touch_n=3
step_8_converted = COUNT DISTINCT user_id from `converted` WHERE scenario=X AND timestamp in window

opted_out_total = COUNT DISTINCT user_id from `opted_out` WHERE scenario=X
escalated_total = COUNT DISTINCT user_id from `escalated` WHERE scenario=X
bad_feedback_total = COUNT DISTINCT user_id from `bad_feedback` WHERE scenario=X
undeliverable_total = COUNT DISTINCT user_id from `touch.send_failed` WHERE touch_n=1
expired_total = COUNT DISTINCT user_id from `sequence.expired` WHERE scenario=X
exhausted_total = COUNT DISTINCT user_id from `sequence.exhausted` WHERE scenario=X
```

**Window definition**: by default, the window applies to the `touch.sent (touch_n=1)` event — i.e., users who entered the funnel within the window. All downstream metrics include those users' subsequent events even if they fall outside the window (within 30 days post-entry).

---

## Drop-off rates (computed visualizations)

For each transition:

```
drop_2_to_3 = 1 - (step_3 / step_2)           // touch 1 → touch 1 reply
drop_3_to_4 = 1 - (step_4 / (step_2 - step_3))// touch 1 no-reply → touch 2 sent (should be ~100% modulo conversions/opt-outs)
drop_4_to_5 = 1 - (step_5 / step_4)           // touch 2 → touch 2 reply
drop_5_to_6 = 1 - (step_6 / (step_4 - step_5))// touch 2 no-reply → touch 3 sent
drop_6_to_7 = 1 - (step_7 / step_6)           // touch 3 → touch 3 reply
drop_to_conversion = 1 - (step_8 / (step_3 + step_5 + step_7))  // any reply → conversion
```

These drop-off rates power the "where users are leaving" visualization.

---

## Per-scenario funnel customizations

### C1 — Cold outreach
- Step 1 (eligible) often >> step 2 (reached) because of suppression matrix
- Track variant breakdown: A (reintroduction) vs B (problem-first)

### C2 — Trademobile active w/ fines
- Track fine_count_bucket breakdown: single / multiple / high
- Conversion target plan: typically VIP (₪489)

### C3 — Past customer winback
- Track lapse_recency breakdown: fresh / recent / cold
- Coupon issuance happens only at touch 3 — track separately

### C4 — Trademobile welcome
- **Touch 2 fires for everyone**, not just no-reply users — drop-off rate at step 3 is informational, not a leak
- Step 8 (conversion) typically lags by 30+ days — this is a long-tail attribution scenario
- Use a longer attribution window for C4 (60 days, not 14)

### C5 — Free user got fine
- Real-time scenario — funnel measured in hours, not days, for first 24h
- Track dual-CTA breakdown: one-off vs VIP conversion
- Handoff-to-C7 is its own step (between exhausted and re-entered)

### C6 — Pre-expiry retention
- 4-touch sequence (not 3); funnel has an additional step 8' for touch 4 (day-of last call, no coupon)
- Track auto-renew conversion separately from plan-change conversion

### C7 — Dirty winback
- Single coupon (`SAVE30`, 30% off the appeal) — no ladder, no `SAVE50`
- **Cannibalization view**: share of appeal conversions coming through the `SAVE30` coupon vs. organic

---

## B1 funnel (different shape)

B1 isn't sequential — it's branching by intent.

```
                              b1.session_started
                                     │
              ┌────────┬──────┬─────┴─────┬──────┬──────┬──────┬──────┬──────┐
             I1       I2     I3          I4     I5     I6     I7     I8     I9
       fine_received what  pricing    detection acct  appeal complaint human fallback
              │       │     │           │      │     │      │       │      │
        data collected     diagnostic                                     1 retry
              │       │     │           │      │     │      │       │      │
         routed/      ...   plan         ...  esc   esc   esc/      esc    esc
         converted/                                          bad_fb
         escalated
```

**B1 funnel metrics:**
- Sessions started (volume)
- Intent distribution (% per intent)
- Per-intent resolution: conversion / escalation / dropped
- Classification failure rate (% routed to I9_fallback)
- Conversion rate per intent

---

## User-level views (the "who" panel)

This view doesn't show aggregate numbers — it shows lists of individual users.

### View 1: Users currently mid-sequence

```sql
SELECT user.name, user.phone, scenario, current_touch_n, days_in_sequence
FROM users
JOIN current_sequence_state
WHERE state IN ('entered', 'replied') AND scenario IN (C1..C7)
ORDER BY days_in_sequence DESC
```

### View 2: Users who replied to touch N

```sql
SELECT user.name, user.phone, scenario, touch_n, reply_text, reply_ts
FROM events
WHERE event_type = 'touch.replied' AND touch_n = <N> AND timestamp in window
ORDER BY reply_ts DESC
```

(N = 1, 2, or 3 — toggle in UI.)

### View 3: Bad-feedback users

```sql
SELECT user.name, user.phone, user.subscription, scenario, signal_type, reply_text, timestamp
FROM events
WHERE event_type = 'bad_feedback' AND timestamp in window
ORDER BY timestamp DESC
```

### View 4: Opted-out users

```sql
SELECT user.name, user.phone, user.subscription, scenario_at_opt_out, trigger_phrase, timestamp
FROM events
WHERE event_type = 'opted_out' AND timestamp in window
ORDER BY timestamp DESC
```

### View 5: Pending escalations

```sql
SELECT user.name, user.phone, scenario, escalation_reason, urgency, timestamp, time_since_escalation
FROM events
WHERE event_type = 'escalated' AND no subsequent 'human_resolved' event
ORDER BY urgency DESC, timestamp ASC
```

---

## Cohort comparison

Each cohort (Trademobile-warm / cold / lapsed / active-vip / active-detection) has its own funnel computed the same way, restricted to users whose `acquisition_source` or `subscription_history` matches the cohort definition.

**Side-by-side view in dashboard**: 3 columns showing top-3 cohorts' funnels for the same scenario, so Yossi can compare. Default cohorts: Trademobile-warm vs cold vs lapsed.

**Cross-cohort analysis question example**: "C5 reply rate for Trademobile-warm vs cold leads" — if Trademobile-warm is dramatically higher, the cold list isn't worth the volume.

---

## Limitations the dashboard cannot answer

Setting expectations up front — these are gaps that require additional data sources:

- **Why** users opted out (beyond the trigger phrase). Need user research, not event data.
- **Whether** appeal succeeded. Comes from appeal system, not the bot. Out of scope this round.
- **LTV** of converted users post-month-1. Comes from billing system.
- **Comparison to prior bot vendor**. We don't have historical events from the legacy stack in this schema. The dashboard starts measuring from go-live forward.
- **Real-time WhatsApp delivery / read rates** — depend on WhatsApp API tier; not all installations support them.

---

## Sample funnel — C5, last 7d (illustrative numbers)

(Realistic-feeling fake data for the mockup. **NOT** actual Road Protect numbers.)

```
C5 — Free user got a fine | Last 7 days

  Eligible (trigger fired):                  1,247
  ↓ (suppressed by other scenario: 38)
  Reached (touch 1 delivered):               1,209
  ↓
  Touch 1 replied:                             406  (33.6%)
  ↓ (no reply: 803 → touch 2)
  Touch 2 sent:                                803
  ↓
  Touch 2 replied:                              97  (12.1%)
  ↓ (no reply: 706 → touch 3)
  Touch 3 sent:                                706
  ↓
  Touch 3 replied:                              42  (5.9%)
  ↓
  Converted (any touch):                       189  (15.6% of reached)
       — via one-off (₪49):                     67
       — via VIP (₪489):                       122
       Revenue: ₪67,225

Side branches:
  Opted out:                                    18  (1.5%)  ✓ within guardrail
  Bad feedback flagged:                          9  (0.7%)  ✓ within guardrail
  Escalated:                                    14  (1.2%)
  Undeliverable:                                 5  (0.4%)
  Lost to authority (paid externally):          73  (6.0%)
  Exhausted (no reply by touch 3 end):         594
```

---

## Open questions

1. **Attribution window** — 14 days standard, 60 days for C4. Is this right or should C6 also use a longer window (since pre-expiry can convert post-expiry)?
2. **De-dup across re-entries** — if a user enters C3 twice (lapsed, then re-converted, then lapsed again), do we count them once or twice in the 30d funnel? Suggest: once per (user, scenario, entry_correlation_id) — count the entries, not the users.
3. **Suppression visualization** — show the suppressed count as a "leaked" branch, or only as a footnote? Suggest footnote — keeping the main funnel clean.
