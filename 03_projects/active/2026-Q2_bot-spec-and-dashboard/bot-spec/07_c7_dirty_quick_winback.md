# C7 — "Dirty & Quick" Winback / Appeal Abandonment (v2)

**Scenario code**: `C7`
**Channel**: WhatsApp, C2B outbound
**Audience**: Users who **started a single appeal in our system and abandoned it before payment** (status = `basic_details` / `violation_details`); secondary path: users who viewed a fine in the app and didn't start checkout
**Goal**: Get them to **complete the appeal they started**, using a 30% coupon on the appeal. **Not** a VIP pitch — VIP upsell is a separate, later flow after they've experienced the system.
**Tone**: Direct, slightly urgent, transactional but human. "Dirty" = fast and pragmatic, not deceptive. **The highest-risk scenario for over-sell — audit constantly.**

---

## ⚠️ Coupon rule (Yossi's decision — chat 28/04–30/04)

This overrides the earlier v2 draft of this file, which used a 30%→50% coupon ladder on VIP. That was wrong:

- The only coupon is **`SAVE30` = 30% off the one-off appeal (₪49)**. **Never on VIP.**
- **No `SAVE50`, no 50%, no ladder, no high-LTV escalation.** "We never agreed on 50%" (Yossi). One coupon per message; don't offer the user a choice of discounts.
- The discount is on the **current appeal** — say so explicitly. Conversion is **gradual**: close the cheap appeal first so they experience the system end-to-end, *then* a separate later flow upsells VIP. A user who wouldn't pay for one appeal won't jump to an annual subscription.
- These (appeal-abandoners) are the only cohort that gets a coupon at all. Cold / no-fine / pre-expiry / lapsed cohorts get **no coupon** — VIP is already low-priced.

---

## Critique of current version (`06_bot/scenarios/c2b/07_dirty_and_quick_winback.md`)

What was weak in the original (and now fixed here):

1. **Single-touch with the coupon burned on touch 1.** No room to first see if a plain reminder closes them. → multi-touch: touch 1 nudges (no coupon), touch 2 introduces the 30% appeal coupon, touch 3 is a last-call on the *same* coupon (no escalation).
2. **No machine-readable definition of "abandoned."** → trigger predicate below keys off appeal status + time.
3. **`SAVE30` flagged as "example only."** → integration open question retained.
4. **"ראיתי שהצצת בפרטי הדוח" reads surveillance-y.** → reframed to "the appeal you started," which is literally true (they began the flow with us).

---

## Trigger predicate

```
TRIGGER (C7) — path A: abandoned appeal flow
  user.appeal_status IN ('basic_details', 'violation_details')   -- started, didn't pay
  AND user.appeal.checkout_completed = FALSE
  AND user.appeal.last_activity_at <= NOW() - INTERVAL '24 hours'
  AND user.appeal.last_activity_at >= NOW() - INTERVAL '14 days'
  AND user.opted_out = FALSE
  AND NOT EXISTS (C7 sent for this appeal already)
```

```
TRIGGER (C7) — path B: viewed fine in app, didn't start an appeal
  EXISTS (app_event WHERE type = 'fine_detail_viewed' AND user_id = user.id)
  AND that view occurred BETWEEN NOW() - INTERVAL '48 hours' AND NOW() - INTERVAL '2 hours'
  AND NOT EXISTS (appeal_started WHERE user_id = user.id AND created_at > that view)
  AND user.opted_out = FALSE
  AND NOT EXISTS (C5 currently entered/replied)
```

**One C7 per appeal/fine, lifetime.** No re-running.

---

## Variables used

- `{{name}}`, `{{fine.violation_type}}`, `{{fine.amount}}`
- `{{appeal_link}}` — link back into the appeal flow the user started (single-fine appeal, ₪49)
- `{{coupon_code}}` — always `SAVE30` (there is no second code and no `coupon_pct` variable — the discount is fixed at 30% on the appeal)

---

## Sequence

### Touch 1 — Nudge, no coupon

**Delay**: 24h after C7 trigger
**Variants**: A (single)
**Skip conditions**: opted out | converted | appeal paid | escalated
**Events emitted**: standard

```
היי {{name}}, כאן צוות Road Protect 🛡️

ראיתי שהתחלת אצלנו תהליך ערעור על הדוח של {{fine.violation_type}} אבל לא סגרנו את זה. חבל להשאיר פתוח — דוח שלא מטופל בזמן צובר ריבית פיגורים של 50% וממשיך להסתבך.

רוצה שנסיים את הערעור? כל מה שנשאר זה להשלים את התהליך כאן: {{appeal_link}}

או שיש משהו ספציפי שעצר אותך?
```

**Why this is better than the original**: removes the "ראיתי שהצצת" surveillance phrasing; doesn't burn the coupon; focuses on the one goal — finishing the appeal.

---

### Touch 2 — 30% coupon on the appeal

**Delay**: +3 days after touch 1
**Variants**: A (single)
**Coupon issued**: `SAVE30`, 30% **on the appeal**
**Skip conditions**: standard
**Events emitted**: standard + `coupon.issued: SAVE30`

```
היי {{name}}, אני מבין שאולי המחיר הוא העיכוב.

סידרתי לך 30% הנחה על הערעור הנוכחי — הקוד: {{coupon_code}}. תקף 7 ימים.

המומחים שלנו ייקחו מכאן את הטיפול וילחמו למקסם את סיכויי ביטול הדוח והנקודות עבורך. כל מה שצריך זה להשלים את הערעור כאן: {{appeal_link}}

אם עדיין לא מתאים — אין בעיה. רק תכתוב לי "הסר" אם תרצה גם להסיר את עצמך מהתראות.
```

> Note: the coupon is on the **appeal**, not VIP. Don't mention VIP pricing here — the goal is to close the appeal the user already started.

---

### Touch 3 — Last call (same coupon, no escalation)

**Delay**: +5 days after touch 2
**Variants**: A (single)
**Coupon**: still `SAVE30` — **no bigger discount.** This is a deadline reminder, not a new offer.
**Exit conditions**: after sending → `exhausted` (no new C7 for this appeal)
**Events emitted**: standard

```
היי {{name}}, פעם אחרונה ממני בנושא הזה.

הקוד {{coupon_code}} (30% על הערעור) תקף עוד יומיים. אחרי זה הדוח פשוט ממשיך לצבור ריבית פיגורים, וחבל.

אם זה הזמן — מסיימים כאן בכמה דקות: {{appeal_link}}. ואם לא — לא אחזור על זה.
```

---

## After they convert — gradual VIP upsell (separate flow, NOT here)

Once the user completes the appeal and experiences the system end-to-end, a **separate, later** flow offers VIP. Do not cram a subscription pitch into the abandoned-appeal sequence (Yossi, 30/04: a user who balked at one appeal won't jump straight to an annual plan; be pointed on the current appeal).

---

## Branches

### B1 — "How do I use the coupon?"
```
פשוט: כנס/י ל-{{appeal_link}}, ובמעמד התשלום יש שדה להזין את הקוד {{coupon_code}}. המחיר יתעדכן אוטומטית עם 30% הנחה על הערעור. ברגע שתסיים/י, המומחים שלנו מקבלים את הדוח ומתחילים לטפל מיד.
```
**Event**: `branch.taken: coupon_redemption_help`

### B2 — "Why appeal and not just pay?"
```
אם תשלם עכשיו, אתה מודה בעבירה — והנקודות נצברות ברישיון. הנקודות מובילות לקורסי נהיגה מונעת או פסילה ברגע שהן עוברות סף. ערעור מנסה לבטל את הקנס *והנקודות* במקביל.

עם 30% ההנחה על הערעור, זה יוצא ממש זול יחסית למה שדוח לא מטופל יכול לעלות לך. שווה ניסיון, לא?
```
**Event**: `branch.taken: pay_vs_appeal`

### B3 — "I'll think about it"
```
בכיף. הקוד {{coupon_code}} תקף עוד כמה ימים. אם תרצה — אני כאן. אם לא, אין בעיה.
```
**No further nudge** beyond the scheduled touches. **Event**: `branch.taken: thinking`

### B4 — Price objection ("עדיין יקר")
```
אני מבין. אבל שווה לחשוב כמה עולה לך *לא* לטפל בדוח — הקנס עצמו + ריבית פיגורים של 50% + נקודות שיכולות לחייב קורס נהיגה מונעת. עם 30% ההנחה, הערעור יוצא זול בהרבה מהסיכון. רוצה שנעבור על זה ביחד?
```
**Event**: `branch.taken: still_too_expensive`, `objection.raised: price`

### B5 — "הפסיקו לשלוח לי"
```
מובן. אני עוצר את ההודעות בנושא הזה. אם תרצה להסיר את עצמך לחלוטין מההתראות, תכתוב "הסר" ואני אדאג לזה.
```
Set status `escalated` if borderline (anger), `opted_out` if explicit opt-out phrase. **Event**: `branch.taken: push_back_strong`, possibly `bad_feedback`

### B6 — Coupon already used / expired
```
זה מוזר — תוודא/י רגע שזה הקוד הנכון. אם עדיין לא עובד, אעדכן עם הנציג ונחזור אליך. תרצה/י?
```
Escalate to human. **Event**: `branch.taken: coupon_failed`, `escalated: coupon_issue`

### B7 — Opt-out / B8 — Identity / B9 — Other
Standard.

---

## Anti-cannibalization rules

The dashboard must track these to flag if C7 hurts full-price / appeal conversion:

1. **No C7 to users who would trigger C5 within 24h** — C5 owns the fresh-fine moment.
2. **No more than 2 C7 sequences per user per 365 days** — protects against coupon-conditioning.
3. **If a user converts on a C7-issued coupon, flag them in CRM** — for retention monitoring (do coupon-converts churn / never upgrade to VIP?).
4. **Track the share of appeal conversions that came via `SAVE30`** — guardrail against training the audience to wait for the discount.

---

## Suppression and exit

- **C5 fires while C7 in flight**: C5 wins.
- **Appeal paid externally / fine paid to authority during C7**: sequence ends (`expired` / `converted_external`).
- **Conversion at any touch**: `converted` with product = `one_off_appeal`, revenue, `coupon_used` (boolean).
- **Exhausted after touch 3**: no more C7 for this appeal.

---

## Events emitted

Standard + C7-specific:
- `coupon.issued: SAVE30` — touch 2 (and referenced again at touch 3)
- `coupon.redeemed` — joined from checkout (product = appeal)
- `coupon.cannibalization_check` — daily aggregate: share of appeal conversions via `SAVE30` vs. organic

---

## A/B testing slots

- **Touch 1 no-coupon vs touch 1 with the 30% coupon** — does waiting one touch before the coupon outperform leading with it?
- **Touch 2 timing**: +3d vs +5d after touch 1
- **Touch 1 framing**: "התחלת תהליך ולא סיימת" vs "הדוח עדיין פתוח"

*(No 50%-framing test — there is no 50% coupon.)*

---

## Open questions for Yossi

1. **`SAVE30` code** — live, real, integrated on the appeal-checkout? The original flagged it as "example only." Need a real working code on the ₪49 appeal product.
2. **Abandonment threshold** — is 24h→14d the right window for path A? And does the app emit `fine_detail_viewed` for path B, or does path B need instrumentation first?
3. **Hand-off to the VIP upsell flow** — once an appeal is completed via C7, how long before the (separate) VIP upsell flow fires?
