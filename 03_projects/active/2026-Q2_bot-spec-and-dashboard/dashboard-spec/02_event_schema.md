# 02 — Event Schema

*The canonical event taxonomy. Every event the bot emits to power the dashboard.*

**Audience**: vendor implementing the bot AND dashboard.

---

## Schema principles

1. **Every state transition emits exactly one event.** No silent transitions.
2. **Every event has a consistent envelope** (see § Envelope). The `payload` differs per event type.
3. **Events are immutable.** Corrections are new events, not edits.
4. **No PII outside the `user_identity` envelope field.** Reply text is allowed but considered sensitive.
5. **Timezone**: all timestamps stored in UTC; rendered in `Asia/Jerusalem` in the dashboard.

---

## Envelope (every event has these fields)

```json
{
  "event_id": "uuid",                           // unique per event
  "event_type": "touch.sent",                   // see § Event types
  "schema_version": "1.0",                      // for forward-compat
  "timestamp_utc": "2026-05-26T14:32:11Z",
  "user_identity": {
    "user_id": "internal_id",                   // CRM stable id
    "phone": "+972...",                         // E.164
    "name": "Yossi",                            // first name, if known
    "subscription": "trademobile_free"          // current subscription at event time
  },
  "scenario": "C5",                             // C1..C7 or B1
  "touch_n": 1,                                 // null for non-touch events
  "variant": "A_speed",                         // null if no A/B
  "correlation_id": "uuid",                     // session/conversation id
  "payload": { ... }                            // event-specific (see § per-event)
}
```

---

## Event types (canonical list, alphabetical for lookup)

### `b1.session_started`
Fired when an inbound user message starts a new B1 session.
- **Payload**: `{ "first_message_text": "<sanitized>", "user_session.b1_active": true }`

### `b1.session_ended`
After 12h of silence OR explicit "תודה, סיימנו" from user.
- **Payload**: `{ "session_duration_seconds": int, "message_count": int }`

### `b1.intent`
Fired when bot classifies an inbound message into an intent.
- **Payload**: `{ "intent_id": "I1_fine_received", "confidence": 0.92, "classifier": "phrase|llm" }`

### `b1.data_collected`
Fired when multi-turn data-gathering completes (I1 or I5).
- **Payload**: `{ "fields": {"when": "...", "violation_type": "speed", "amount": 750} }`

### `bad_feedback`
Fired when user reply matches bad-feedback signal (per `bot-spec/00_overview.md` § 0.16).
- **Payload**: `{ "signal_type": "complaint_phrase|cancellation_intent|abusive|legal_threat|sentiment_classifier", "reply_text": "<full text>", "matched_phrase": "if applicable" }`

### `branch.taken`
Fired when bot routes a reply into a specific branch (B1/B2/...).
- **Payload**: `{ "branch_id": "fine_specific|pricing_question|...", "reply_text_sample": "<first 200 chars>" }`

### `bucket.assigned`
Fired when fine-count or lapse-recency segmentation flag is computed.
- **Payload**: `{ "bucket_type": "fine_count|lapse_recency", "bucket_value": "single|multiple|high" }`

### `cap_deferred`
Fired when a planned touch is deferred due to frequency cap.
- **Payload**: `{ "cap_type": "24h|7d|30d", "would_be_touch_n": 2, "deferred_until_utc": "..." }`

### `converted`
Fired when a user converts (subscribes / upgrades / appeals).
- **Payload**: `{ "plan": "vip|detection|one_off", "revenue_ils": 489, "touch_attributed_to": 2, "coupon_used": true, "coupon_code": "SAVE30", "checkout_id": "..." }`

### `coupon.issued`
Fired when bot sends a coupon (**C7 only** — `SAVE30`, 30% off the ₪49 appeal). No coupons in C3/C6; no `SAVE50`.
- **Payload**: `{ "coupon_code": "SAVE30", "coupon_pct": 30, "product": "one_off_appeal", "expires_utc": "..." }`

### `coupon.redeemed`
Fired when appeal checkout completes with a bot-issued coupon code.
- **Payload**: `{ "coupon_code": "SAVE30", "discount_ils": 15, "net_revenue_ils": 34, "product": "one_off_appeal" }`

### `escalated`
Fired when bot hands off to human.
- **Payload**: `{ "reason": "legal_threat|refund|human_request|...", "urgency": "high|medium|low", "handoff_packet": {...} }`

### `fine.detected` *(upstream — not bot's own emission)*
Referenced for C5 trigger. Vendor's bot consumes; dashboard joins on it.
- **Payload**: `{ "fine_id": "...", "user_id": "...", "violation_type": "speed", "amount_ils": 750, "authority": "police|tel_aviv_muni|..." }`

### `handoff.to.c7`
Fired when C5 sequence exhausts and user is eligible for C7-A.
- **Payload**: `{ "previous_scenario": "C5", "fine_id": "..." }`

### `objection.raised`
Fired when reply matches an entry in objection library.
- **Payload**: `{ "objection_id": "price|distrust|not_needed|already_paid|...", "matched_phrase": "..." }`

### `opted_out`
Fired when user opts out.
- **Payload**: `{ "reason": "user_request", "trigger_phrase": "הסר אותי", "from_scenario": "C5" }`

### `re_subscribed`
Fired when opted-out user re-opts in via B1.
- **Payload**: `{ "previously_opted_out_at_utc": "...", "consent_text": "..." }`

### `scenario.eligible`
Fired when trigger predicate is satisfied for a user (before suppression).
- **Payload**: `{ "trigger_predicate_match": {...} }`

### `scenario.suppressed`
Fired when eligible but blocked by suppression matrix.
- **Payload**: `{ "suppressed_by": "C5", "suppression_reason": "fresh_fine_priority" }`

### `sequence.completed`
Fired when scenario reaches a normal end (not exhaustion). C4 uses this.
- **Payload**: `{ "final_touch_n": 2, "final_state": "completed" }`

### `sequence.exhausted`
Fired when all planned touches sent + grace period elapsed with no reply.
- **Payload**: `{ "last_touch_n": 3, "grace_period_hours": 24, "next_eligibility_at_utc": "..." }`

### `sequence.expired`
Fired when trigger window passed (e.g. fine paid before C5 could close).
- **Payload**: `{ "reason": "fine_paid_externally|trademobile_year_lapsed|other" }`

### `session.state_changed`
Fired on any user session state transition (per `bot-spec/09_cross_cutting.md` § 9.1).
- **Payload**: `{ "from_state": "idle", "to_state": "c2b_active", "trigger": "C5_entered" }`

### `touch.delivered`
Fired when WhatsApp returns a delivery receipt.
- **Payload**: `{ "delivery_ts_utc": "...", "whatsapp_message_id": "..." }`

### `touch.read`
Fired when WhatsApp returns a read receipt (if API supports).
- **Payload**: `{ "read_ts_utc": "..." }`

### `touch.replied`
Fired when user replies to a specific touch.
- **Payload**: `{ "reply_text": "<full text>", "reply_ts_utc": "...", "reply_message_id": "..." }`

### `touch.send_failed`
Fired when WhatsApp send fails.
- **Payload**: `{ "error_code": "...", "error_reason": "invalid_number|user_blocked|template_rejected|..." }`

### `touch.sent`
Fired when bot dispatches an outbound message to WhatsApp.
- **Payload**: `{ "message_text": "<full Hebrew text as sent>", "template_id": "...", "links_included": ["..."], "utm_params": {...} }`

### `variable_resolution_failed`
Fired when a required variable can't resolve (per § 9.2).
- **Payload**: `{ "variable_name": "{{plate}}", "scenario": "C5", "touch_n": 1, "action_taken": "skip_touch|alert_ops" }`

### `welcome.sent` *(C4-specific)*
Alias for `touch.sent` when touch_n=1 and scenario=C4. Emitted in addition for funnel-start tracking.

### `month_1_checkin.sent` *(C4-specific)*
Alias for `touch.sent` when touch_n=2 and scenario=C4.

### `expiry.30d.sent` / `expiry.14d.sent` / `expiry.3d.sent` / `expiry.day_of.sent` *(C6-specific)*
Aliases for C6 touches. Allows the renewal-funnel view to align by relative-to-expiry timing rather than absolute time.

---

## Special: reply-text storage

The `reply_text` field in `touch.replied` and `bad_feedback` events stores the user's full message. Considerations:

- **Sensitive PII**: treat reply text as private. Dashboard masks it for non-authenticated views.
- **Retention**: 24 months. After that, hash-anonymized.
- **Search**: dashboard indexes reply text for sentiment, objection-detection, and ad-hoc queries.
- **Encryption at rest**: required (per `01_business_context/LEGAL_DISCLAIMER.md` — data security commitments).

---

## Special: `correlation_id` rules

The `correlation_id` ties together events from a single user conversation. Rules:

- New C2B sequence start → new `correlation_id`
- Touch 2, touch 3 → same `correlation_id` as touch 1
- User reply to any touch → same `correlation_id`
- B1 session start (user-initiated inbound) → new `correlation_id`, *unless* user is mid-C2B in which case **reuse the active C2B `correlation_id`** (so the conversation is one thread)
- `escalated` event → same `correlation_id` as the trigger event
- `converted` event → joined to most recent active `correlation_id` (within last 14 days)

---

## Conversion attribution rule

The `touch_attributed_to` field in the `converted` payload is computed as:

1. **If user clicked a UTM-tagged link from a specific touch within last 14 days**: attribute to that touch.
2. **Else if user replied to a specific touch within last 14 days**: attribute to that touch.
3. **Else if user received any touch within last 14 days**: attribute to the most recent touch.
4. **Else**: organic / no-attribution. Mark `touch_attributed_to = null`, `attribution_source = 'organic'`.

This **window is 14 days**. Conversions outside the window get no attribution.

---

## Ingestion contract for the vendor

The vendor's bot emits events to a single events endpoint. Required:

- **Format**: JSON-line (one event per line)
- **Endpoint**: TBD (Road Protect-hosted or vendor's webhook back to us)
- **Latency**: events must arrive within 60 seconds of fire
- **Idempotency**: events must include `event_id` so re-sends don't double-count
- **Order**: events do not need to arrive in order; dashboard sorts on `timestamp_utc`
- **Retry**: if endpoint is down, vendor must retry with exponential backoff up to 24h
- **Schema validation**: malformed events are quarantined to a deadletter queue, not silently dropped

---

## Schema versioning

Current: `schema_version = "1.0"`.

Breaking changes (e.g. removing a payload field) require:
1. Bumping `schema_version`
2. Vendor + dashboard both updated before the change ships
3. Backward-compat read window for 30 days

---

## What to do when the schema is unclear

When the vendor finds a scenario action that doesn't map cleanly to an event in this list:
- **Don't invent a new event silently**.
- **Flag in the open-questions list** during onboarding.
- **Get explicit sign-off** before extending the schema.

---

## Open questions for Yossi / vendor

1. **Events endpoint location**: hosted by Road Protect, by vendor, or third party (Segment, Mixpanel, RudderStack)?
2. **Sentiment classifier integration**: does the vendor's stack include a sentiment model, or do we add an external one? Affects `bad_feedback` precision.
3. **Conversion attribution window**: 14 days reasonable, or shorter? (Longer = more conversions credited to outbound; shorter = cleaner causality.)
4. **Reply text retention**: 24 months — is that aligned with company-wide PII retention policy?
