# 01 — Metrics Glossary

*The canonical definition of every metric the dashboard surfaces. If the dashboard shows a number, it has a row here.*

**Audience**: Yossi (for reading), the vendor (for implementation).

---

## How to read this doc

Each metric has:
- **Name** — exact label as it appears in dashboard
- **Definition** — what it measures, in plain language
- **Formula** — how to compute it from event data
- **Window** — default time window (overridable in UI: 7d / 30d / 90d / all-time)
- **Slice-by** — dimensions the metric can be broken down on
- **Why we care** — the decision it informs

---

## Funnel metrics — top of stack

These are the primary user-flow metrics. Every C2B scenario gets a funnel; B1 gets a parallel funnel-by-intent.

### `reached_count`

- **Definition**: Number of unique users for whom touch 1 of the scenario was sent successfully (delivered to WhatsApp).
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'touch.delivered' AND scenario = X AND touch_n = 1 AND timestamp BETWEEN window`
- **Window**: default 30d
- **Slice-by**: scenario, variant, fine_count_bucket (where applicable), lapse_recency (C3), cohort
- **Why we care**: top of funnel — how many users we actually contacted

### `touch_1_replied_count`

- **Definition**: Number of unique users who replied to touch 1 of the scenario at least once.
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'touch.replied' AND scenario = X AND touch_n = 1 AND timestamp BETWEEN window`
- **Slice-by**: scenario, variant
- **Why we care**: first-message landing — does the opener get engagement?

### `touch_2_sent_count`

- **Definition**: Number of unique users for whom touch 2 was sent. (Excludes users who replied to touch 1 and were skipped from touch 2.)
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'touch.sent' AND scenario = X AND touch_n = 2 AND timestamp BETWEEN window`
- **Why we care**: how big is the "no-reply nudge" cohort?

### `touch_2_replied_count`

Same as touch_1_replied_count but for touch 2. Useful for distinguishing "responded immediately" from "needed a nudge."

### `touch_3_sent_count` / `touch_3_replied_count`

Same as above but touch 3.

### `converted_count`

- **Definition**: Number of unique users who converted during the scenario (subscribed / upgraded / appealed).
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'converted' AND scenario = X AND timestamp BETWEEN window`
- **Slice-by**: scenario, plan (one_off / detection / vip), touch_attributed_to (which touch was the last one before conversion)
- **Why we care**: the conversion outcome — primary success signal per scenario

### `converted_revenue_ils`

- **Definition**: Total ILS revenue from conversions attributed to this scenario.
- **Formula**: `SUM(payload.revenue_ils) WHERE event_type = 'converted' AND scenario = X AND timestamp BETWEEN window`
- **Slice-by**: scenario, plan, touch
- **Why we care**: dollar (shekel) value of the scenario

### `opted_out_count`

- **Definition**: Number of users who triggered opt-out during the scenario.
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'opted_out' AND scenario = X AND timestamp BETWEEN window`
- **Why we care**: **guardrail metric** — we want this LOW. If it spikes per scenario, the cadence or copy is wrong.

### `bad_feedback_count`

- **Definition**: Number of users who flagged bad-feedback signal (per § 0.16).
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'bad_feedback' AND scenario = X AND timestamp BETWEEN window`
- **Slice-by**: scenario, signal type (complaint phrase / cancellation intent / abusive / legal threat / sentiment)
- **Why we care**: **guardrail metric** — signals if the bot is feeling pushy or off-tone

### `escalated_count`

- **Definition**: Number of escalations to human, per scenario.
- **Formula**: `COUNT(DISTINCT user_id) WHERE event_type = 'escalated' AND scenario = X AND timestamp BETWEEN window`
- **Slice-by**: scenario, reason
- **Why we care**: operational load on human team + signals where bot is underpowered

---

## Funnel metrics — derived ratios

### `touch_1_reply_rate`

- **Formula**: `touch_1_replied_count / reached_count`
- **Why we care**: opener strength. Target ≥ 8% for C2B cold (C1, C3-cold) and ≥ 20% for warm scenarios.

### `touch_2_reply_rate`

- **Formula**: `touch_2_replied_count / touch_2_sent_count`
- **Why we care**: does the nudge work? **This is the number Yossi explicitly asked to see.**

### `touch_3_reply_rate`

- **Formula**: `touch_3_replied_count / touch_3_sent_count`
- **Why we care**: closer effectiveness

### `conversion_rate`

- **Formula**: `converted_count / reached_count`
- **Why we care**: end-to-end efficacy

### `conversion_rate_per_touch`

- **Formula**: `converted_count_attributed_to_touch_n / touch_n_replied_count`, for n ∈ {1,2,3}
- **Why we care**: where in the sequence does conversion actually happen? Tells us if we can shorten the sequence or where to focus copy work.

### `opt_out_rate`

- **Formula**: `opted_out_count / reached_count`
- **Guardrail**: ≤ 2% per scenario per month. If higher, slow the scenario.

### `bad_feedback_rate`

- **Formula**: `bad_feedback_count / reached_count`
- **Guardrail**: ≤ 1% per scenario per month.

---

## Revenue metrics

### `revenue_per_user_reached_ils`

- **Formula**: `converted_revenue_ils / reached_count`
- **Why we care**: economic efficiency of the scenario per user contacted

### `revenue_per_reply_ils`

- **Formula**: `converted_revenue_ils / (touch_1_replied_count + touch_2_replied_count + touch_3_replied_count)`
- **Why we care**: of users who engaged at all, how much revenue per engagement

### `revenue_per_message_sent_ils`

- **Formula**: `converted_revenue_ils / SUM(touch_n_sent_count)` for all n
- **Why we care**: cost efficiency — every message costs something (vendor fees, opt-out risk)

### `arpu_c2b_30d`

- **Formula**: average revenue per converting user from C2B in last 30 days
- **Why we care**: tells us whether C2B is bringing in high-LTV or low-LTV users

---

## Coupon metrics (C7 only)

*The coupon (`SAVE30`, 30% off the ₪49 appeal) is issued only in C7. C3 and C6 issue no coupons.*

### `coupons_issued_count`

- **Formula**: `COUNT(*) WHERE event_type = 'coupon.issued' AND scenario = X`
- **Slice-by**: scenario, coupon code

### `coupons_redeemed_count`

- **Formula**: `COUNT(*) WHERE event_type = 'coupon.redeemed' AND scenario = X`

### `coupon_redemption_rate`

- **Formula**: `coupons_redeemed_count / coupons_issued_count`
- **Why we care**: are users using the coupon at all?

### `coupon_share_of_conversions`

- **Formula**: `coupons_redeemed_count / total_appeal_conversions`
- **Guardrail**: should stay ≤ 25%. If >25% of appeal conversions ride the coupon, we're conditioning the audience to wait for it.

### `revenue_per_coupon_issued_ils`

- **Formula**: `coupons_redeemed_revenue_ils / coupons_issued_count`
- **Why we care**: economic efficiency of the coupon lever

---

## B1 inbound metrics

### `b1_sessions_started_count`

- **Formula**: `COUNT(DISTINCT correlation_id) WHERE event_type = 'b1.session_started'`
- **Why we care**: inbound volume — are users finding our WhatsApp?

### `b1_intent_distribution`

- **Formula**: percentage of `b1.intent: X` events for each intent X
- **Why we care**: tells us what users actually want when they reach out. Drives priority on which intents to deepen.

### `b1_classification_failure_rate`

- **Formula**: `count(b1.intent: fallback) / count(b1.intent: *)`
- **Guardrail**: ≤ 8%. Higher = LLM classifier underperforming or taxonomy incomplete.

### `b1_to_conversion_rate`

- **Formula**: `count(converted WHERE prior event is b1.session_started in same correlation_id) / b1_sessions_started_count`
- **Why we care**: inbound conversion quality

### `b1_to_escalation_rate`

- **Formula**: `count(escalated in b1) / b1_sessions_started_count`
- **Guardrail target**: between 5%-15%. Below 5% = bot is over-handling (frustrating users with bot when they need a human). Above 15% = bot is under-handling.

---

## User-level views (powers the "who" panel)

### `users_in_state_<state>`

For each state in the state machine (eligible / entered / replied / converted / opted_out / escalated / exhausted / expired / undeliverable):

- **Definition**: list of users currently in that state, per scenario
- **Slice-by**: scenario
- **Why we care**: Yossi's "who replied to message 2, who opted out, who flagged bad feedback" view

### `users_who_replied_at_touch_n`

- **Definition**: list of (user_id, phone, name, scenario, reply_text_sample, timestamp) where the user replied at touch n
- **Why we care**: dashboards's directly-asked-for view ("who replied to the 1st message")

### `users_with_bad_feedback_30d`

- **Definition**: list of users who emitted `bad_feedback` in last 30 days
- **Fields**: user_id, phone, name, scenario context, signal type, exact reply text, timestamp
- **Why we care**: directly-asked-for "bad feedback / wanted to revoke sub and who" view

### `users_who_opted_out_30d`

- **Definition**: list of opt-outs with context
- **Fields**: user_id, phone, name, scenario at time of opt-out, trigger phrase used, was-subscriber-or-prospect

---

## Cohort comparison metrics (for the Cohorts panel)

### `cohort_funnel`

For each cohort (e.g. Trademobile-warm / cold-lead / lapsed):

- All funnel metrics above, restricted to the cohort
- **Why we care**: which cohort produces the highest conversion per shekel of outbound

### `cohort_definitions`

| Cohort | Definition |
|---|---|
| **Trademobile-warm** | `user.acquisition_source = 'trademobile' AND user.subscription IN ('trademobile_free', 'vip')` |
| **Cold lead** | `user.acquisition_source IN ('landing_page', 'partner_referral') AND no prior subscription` |
| **Lapsed** | `user.subscription_history.last_status IN ('cancelled', 'expired')` |
| **Active VIP** | `user.subscription = 'vip'` |
| **Active Detection** | `user.subscription = 'detection'` |

---

## System / health metrics

### `messages_sent_24h`

- **Definition**: total outbound messages in last 24 hours
- **Why we care**: volume monitoring; sudden spikes suggest a bug or trigger storm

### `delivery_failure_rate`

- **Formula**: `count(touch.send_failed) / count(touch.sent)`
- **Guardrail**: ≤ 2%. Higher = phone validation broken or WhatsApp API issues.

### `quiet_hours_deferral_count`

- **Definition**: number of touches deferred to next eligible window
- **Why we care**: how much of our planned volume hits quiet hours

### `cap_deferred_count`

- **Definition**: number of touches deferred by frequency caps
- **Why we care**: are we trying to send too much to specific users?

---

## "What needs my attention" derived metrics

These are the ones that should land Yossi on the right action when he opens the dashboard.

### `scenarios_with_failing_guardrails`

- **Definition**: list of scenarios where `opt_out_rate > 2%` OR `bad_feedback_rate > 1%` OR `delivery_failure_rate > 2%` in last 30d
- **Why we care**: the bot is misbehaving on this scenario; intervene

### `scenarios_with_dropping_reply_rate`

- **Definition**: scenarios where touch-1 reply rate in last 7d is more than 30% below 30d average
- **Why we care**: copy is decaying or audience is fatiguing — refresh or rest

### `users_pending_human_followup`

- **Definition**: list of escalations awaiting human response past SLA
- **Why we care**: operational alert

---

## Definitions of "the things Yossi explicitly asked for"

Mapping the user's original questions to metric IDs:

| Yossi's question | Metric(s) |
|---|---|
| How many users we reached | `reached_count` per scenario |
| How many replied to 1st message | `touch_1_replied_count` per scenario |
| How many replied to 2nd message etc | `touch_2_replied_count`, `touch_3_replied_count` |
| Who replied (specifically) | `users_who_replied_at_touch_n` (list view) |
| How many converted | `converted_count`, `conversion_rate` |
| How many bad feedback / wanted revoke sub | `bad_feedback_count`, `users_with_bad_feedback_30d` (list w/ names) |
| Who had bad feedback | `users_with_bad_feedback_30d` (with exact reply text) |
