# C3 — Past Customer Winback (v2)

**Scenario code**: `C3`
**Channel**: WhatsApp, C2B outbound
**Audience**: Users with a previously paid Road Protect subscription that has lapsed or been cancelled, system has detected ≥1 new fine since lapse
**Goal**: Reactivate with VIP, leverage the detected fine + the past relationship
**Tone**: Warm acknowledgment of the prior relationship, no guilt, concrete proof we never stopped finding things

---

## Critique of current version (`06_bot/scenarios/c2b/03_past_customer_winback.md`)

What's weak in the original:

1. **Identical body to C2.** The original explicitly flags this as "probably leaving money on the table." It is. A lapsed user knows the product — pretending they don't (by using the same copy as a current Trademobile-free user) wastes the strongest leverage we have: shared history.
2. **No tiering by time since lapse.** A 30-day-lapsed user is a different conversation from a 9-months-lapsed user. The original notes this as an open question; spec needs an answer.
3. **No second/third touch + no graceful exit.** Lapsed users with detected fines who don't bite on the first message just go silent — no follow-up, no clean door-close. (Note: a *coupon* is **not** the answer here — per Yossi, the 30% coupon is reserved for single-appeal abandoners only; VIP is not discounted broadly. The fix is more touches and a graceful exit, not a price cut.)
4. **No second touch.** Same single-touch issue.
5. **"Lapse acknowledgment without guilt"** is the right principle but isn't actually executed — the original message reads like the user never had a subscription.

What's strong (kept):

- Recognition that the lapsed-user persona (P5) is distinct from active free-tier (P1/P4).
- The "we never stopped scanning" framing is the correct angle.

---

## Trigger predicate

```
TRIGGER (C3):
  user.subscription_history.last_status IN ('cancelled', 'expired')
  AND user.subscription IS NULL                                          -- not currently paying
  AND user.subscription_history.ended_at >= NOW() - INTERVAL '2 years'   -- not too stale
  AND (
    SELECT COUNT(*) FROM fines
    WHERE fines.user_id = user.id
    AND fines.detected_at >= user.subscription_history.ended_at
    AND fines.status IN ('new', 'open', 'pending_appeal')
  ) >= 1
  AND user.opted_out = FALSE
  AND NOT EXISTS (any higher-priority scenario entered)
```

**Segmentation flag**:

```
lapse_recency =
  CASE
    WHEN ended_at >= NOW() - INTERVAL '60 days' THEN 'fresh'         -- still feels like a customer
    WHEN ended_at >= NOW() - INTERVAL '6 months' THEN 'recent'       -- "haven't seen you in a while"
    WHEN ended_at >= NOW() - INTERVAL '2 years' THEN 'cold'          -- formal reintroduction
  END
```

---

## Variables used

- `{{name}}`, `{{fines_count}}`, `{{plan_link}}`
- `{{months_since_lapse}}` — computed integer, used in `recent` and `cold` variants

> **No coupon in C3.** The 30% coupon is reserved for single-appeal abandoners (C7) and applies to the appeal, not VIP. C3's closer is the value/urgency case at full price (Yossi, chat 16/04).

---

## Sequence

### Touch 1 — Reactivation with concrete proof

**Delay**: 0 from `eligible`
**Variants**: A_fresh, A_recent, A_cold
**Exit conditions**: standard set
**Events emitted**: `touch.sent`, `touch.delivered`, `touch.replied`

#### Variant A_fresh — "we kept watching even after you left"

```
היי {{name}}, כאן Road Protect 🛡️

הצטרפת אלינו בעבר, ואחרי שהמינוי נגמר — המערכת המשיכה לסרוק את המאגרים ברקע (זה חלק מהמודל שלנו). ומאז שעזבת, איתרנו עבורך {{fines_count}} דוחות פתוחים שעדיין דורשים טיפול.

לא רציתי שתלך לאיבוד עם זה. במסלול ה-VIP המומחים שלנו ייקחו את הדוחות האלה — ניסוח ערעור, מאבק על ביטול הקנס והנקודות, סופגים גם ריבית פיגורים שנצברה בינתיים.

רוצה לעבור על הדוחות הספציפיים שאיתרנו?
```

#### Variant A_recent — "haven't seen you in {{months_since_lapse}} months, but you have stuff piling up"

```
היי {{name}}, כאן Road Protect 🛡️

עברו {{months_since_lapse}} חודשים מאז שסיימת איתנו, וברקע המערכת המשיכה לעבוד. איתרנו {{fines_count}} דוחות חדשים על שמך מאז שעזבת — כולם פתוחים, חלק מהם כבר התחילו לצבור ריבית פיגורים.

זה לא הזמן לבזבז עליהם כסף סתם. במסלול VIP המומחים שלנו לוקחים את הסיפור על עצמם — ערעור על כל דוח, ביטול נקודות, וטיפול מול הרשויות.

תרצה שאחזיר אותך פעיל ונתחיל מהדוח הכי דחוף?
```

#### Variant A_cold — "it's been a while, but we found things"

```
היי {{name}}, כאן Road Protect 🛡️

עברה תקופה מאז שהיינו בקשר, אבל מערכת ההגנה שלנו ממשיכה לסרוק את המאגרים. אני סוכן AI דיגיטלי, ופונה כי איתרנו עבורך {{fines_count}} דוחות פתוחים שלא טופלו.

ייתכן שעד היום לא ראית את כל ההודעות הקודמות. הדוחות פעילים — חלקם כבר עם ריבית פיגורים. במסלול VIP אנחנו יכולים לקחת על עצמנו את הטיפול בכולם בבת אחת.

האם תרצה שאחזיר אותך פנימה ונראה איך מנקים את הסיפור הזה?
```

**Quality checklist (touch 1):**
- [x] Acknowledges the prior relationship by name
- [x] Doesn't guilt-trip ("you abandoned us") — uses neutral language
- [x] Cold variant discloses AI explicitly (consistent with C1)
- [x] Concrete number ({{fines_count}}) — proof of value
- [x] Ends with diagnostic / forward question

---

### Touch 2 — Cost-of-waiting reminder

**Delay**: +4 days after touch 1
**Variants**: A (single)
**Skip conditions**: standard
**Events emitted**: standard

```
היי {{name}}, רק להוודא — הדוחות שאיתרנו עדיין פתוחים.

הם לא נעלמים בעצמם. כל יום שעובר מקרב אותם לתאריך כפל הקנס (₪750 שהופך ל-₪1,500), ולסבב גבייה רשמי. המומחים שלנו ב-VIP יודעים בדיוק על איזה סעיפים לערער ברשויות הספציפיות שמטפלות בדוחות שלך.

רוצה לראות איך זה נראה מהצד שלנו? {{plan_link}}
```

---

### Touch 3 — Last call (no coupon)

**Delay**: +7 days after touch 2 (~11 days from touch 1)
**Variants**: A (single)
**Skip conditions**: standard
**Exit conditions**: after sending → `exhausted` (no new C3 for 120 days)
**Events emitted**: `touch.sent`, `touch.delivered`, `sequence.exhausted` (24h after touch 3 if no reply)

> **No coupon.** Per Yossi, VIP isn't discounted to win back lapsed users — the price is already low. The closer is the accumulating-cost reality + a clean door-close, not a price cut.

```
היי {{name}}, פעם אחרונה ממני.

הדוחות שאיתרנו על שמך עדיין פתוחים, והם רק מתקרבים לכפל קנס ולסבב גבייה. המומחים שלנו ב-VIP יכולים לקחת את כל הסיפור על עצמם — ערעור על כל דוח, מאבק על ביטול הקנס והנקודות, וספיגת ריבית פיגורים שנצברה בינתיים.

זה הזמן לעצור את הדוחות שמצטברים. {{plan_link}}

ואם זה לא הזמן, אין בעיה. תכתוב לי "הסר" אם תרצה גם להסיר את עצמך מההתראות שלנו.
```

---

## Branches (when user replies)

### B1 — "I remember you guys / I left because..."
**Bot reply** (acknowledge the reason, then bridge):
```
תודה ששיתפת. הסיבות הכי נפוצות לעזיבה זה מחיר או 'לא נראה לי שאני צריך'. שניהם הגיוניים בזמנו — אבל המספר העכשווי של {{fines_count}} דוחות פתוחים על שמך אומר שזה השתנה.

מה הכי הגיוני להתחיל איתו — דוח ספציפי שהכי דחוף, או לראות את כל התמונה ביחד?
```
**Event**: `branch.taken: lapse_explained`

### B2 — Price objection
Use objection_library response, adjusted to lapsed context. **Don't offer a discount code** — frame around the cost of *not* acting:
```
אני מבין לחלוטין. אבל חשוב להבין: הדוחות הפתוחים כבר עולים כסף בפועל (ריבית פיגורים, נקודות). השאלה היא לא "האם להוציא עוד כסף" אלא "איך לאבד פחות". מספיק שדוח אחד מתבטל וזה מחזיר את עלות המינוי לכמה שנים קדימה. רוצה שאעבור עליהם איתך?
```
**Event**: `branch.taken: price_objection`, `objection.raised: price`

### B3 — "Why did you keep my data after I cancelled?"
This is a legitimate question for a lapsed user. Handle carefully:
```
שאלה טובה. כשמינוי נגמר, אנחנו ממשיכים לסרוק רק את הזיהויים שכבר היו לנו (מספר רכב + ת.ז.) כדי שאם דוח חדש מופיע, נוכל לתת לך את ההזדמנות לטפל בו לפני שהוא הופך לכפל קנס. שמירת המידע היא במסגרת תנאי השימוש שאישרת. אם תרצה שנמחק את הזיהויים שלך לחלוטין — אעביר אותך לנציג שיטפל בזה. רוצה?
```
**Event**: `branch.taken: data_question` — escalate per § 0.12 if user asks for deletion

### B4 — "I sold the car"
**Bot reply:**
```
תודה שעדכנת — חשוב לדעת. הדוחות שאיתרנו על שמך ייתכן והם מתקופה שהרכב היה אצלך, אז עדיין רלוונטיים אליך אישית. אבל אם כולם מתקופה אחרי המכירה, ייתכן והבעיה היא שהבעלות לא הועברה נכון. תרצה שנעבור על הפרטים?
```
**Event**: `branch.taken: car_sold` — may transition to a different sub-flow

### B5 — Opt-out / B6 — Identity check / B7 — Other
Per standard pattern.

---

## Suppression and exit

- C5 (new fine just detected) takes priority — pauses C3.
- If user converts via C3-attributed link: `converted`, scenario ends.
- After touch 3 + 24h no reply: `exhausted`, no new C3 for 120 days.

---

## Events emitted

Standard event set with `scenario = 'C3'`, plus:
- `lapse_recency.assigned` — bucket assigned at trigger time

*(No `coupon.*` events — C3 doesn't issue coupons.)*

---

## A/B testing slots

- **Variant A_fresh / A_recent / A_cold** — already 3-way segmented; can A/B opening lines within each
- **Touch 2 with vs without explicit money math** (₪750 → ₪1,500)
- **Touch 3 framing** — accumulating-cost reality vs "we never stopped scanning" recap (no coupon test — C3 doesn't coupon)

---

## Open questions for Yossi

1. **Lapse-recency boundaries**: 60d / 6m / 2y feels right but worth checking against the actual lapse distribution.
2. **Coupon use in C3** — resolved: **no coupon in C3.** Per Yossi (chat 16/04), the 30% coupon is reserved for single-appeal abandoners (C7) and applies to the appeal, not VIP; VIP isn't discounted broadly. C3 closes on value/urgency at full price.
3. **Cold variant (>1 year lapsed)**: should this even exist, or should >12-month lapsed users get the cold-list treatment (C1) instead? Currently I'm keeping them in C3 because the detected-fine signal is too valuable to waste.
4. **"I sold the car" branch**: this is going to be a real reply — do we have a clean self-service flow for plate updates / account closure post-sale? If not, this becomes an escalation.
