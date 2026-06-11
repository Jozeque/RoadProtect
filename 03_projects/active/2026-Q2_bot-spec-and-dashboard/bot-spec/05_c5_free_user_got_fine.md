# C5 — Free-Tier User Just Got a Fine (v2)

**Scenario code**: `C5`
**Channel**: WhatsApp, C2B outbound, **near-real-time**
**Audience**: User on Detection or Trademobile-free, system just detected a new fine
**Goal**: Empathy → urgency → conversion to VIP (or one-off appeal as fallback)
**Tone**: Empathetic first ("איזה באסה"), strategic second, sales last. Match the user's emotional state — they are *in pain* when this fires.

**Priority**: this is the **highest-priority C2B scenario** (see suppression matrix in `00_overview.md` § 0.5). When C5 fires, it pre-empts everything else.

---

## Critique of current version (`06_bot/scenarios/c2b/05_free_user_got_fine.md`)

What's weak in the original:

1. **No follow-up touch defined for the "didn't convert immediately" path.** A user who saw the alert + the message and didn't pull the trigger needs a follow-up — that's exactly the "abandon" pattern C7 was designed for, but the original C5 doesn't hand off to C7 cleanly.
2. **One-off appeal (₪49) noted in open questions but not offered in the actual message.** This is the biggest miss. A user in fresh-fine panic mode is often NOT ready for a ₪489/year commitment but IS ready for "pay ₪49, we handle this one." Offering both creates a real choice.
3. **Empathy text is well-written but only addresses the speed-camera scenario.** Original notes "match the violation type to the right hook" — but the example response is only for speed. Need at least three template variants (speed / parking / phone / other).
4. **No timing constraint on the "follow up if no reply" beat.** Real-time bot fires, user doesn't reply, then what?
5. **"שלחנו לך עכשיו את פרטי הדוח בצורה נגישה כאן למייל"** is a strange phrase — was the message via email or WhatsApp? Wording is muddy.
6. **Gender-aware variant only written for "speed camera frustration response," not for the original opening.** All opening beats need a gender path.

What's strong (kept):

- Empathy-first principle is exactly right.
- "המון דוחות מתבטלים בגלל טעויות טכניות" is the canonical legal-line-safe framing.
- The 3-month-to-double warning is the right urgency mechanism.

---

## Trigger predicate

```
TRIGGER (C5):
  fine.detected_at >= NOW() - INTERVAL '30 minutes'
  AND fine.status = 'new'
  AND user.subscription IN ('detection', 'trademobile_free')           -- not already VIP
  AND user.opted_out = FALSE
  AND user.phone IS NOT NULL AND user.phone_valid = TRUE
  AND NOT EXISTS (a C5 sent for this fine_id already)                  -- one C5 per fine
```

**Real-time fire constraint**: orchestrator should process within **5 minutes** of `fine.detected_at`, deferring only for quiet hours (see § Quiet hours below).

---

## Variables used

- `{{name}}`, `{{plate}}`, `{{plan_link}}`
- `{{fine.violation_type}}` — `speed | parking | phone | red_light | other`
- `{{fine.amount}}` — ₪ amount
- `{{fine.authority}}` — police / municipality name
- `{{fine.date}}` — violation date
- `{{one_off_appeal_link}}` — separate UTM link for the ₪49 product

---

## Sequence

### Touch 1 — Empathy + dual-CTA (one-off appeal OR VIP)

**Delay**: 0 from `eligible` (real-time)
**Variants**: A_speed, A_parking, A_phone, A_red_light, A_other (by violation type)
**Skip conditions**: none (this is the entry)
**Exit conditions**: `replied` → branches | `opted_out` | continues to touch 2 after 24h no reply
**Events emitted**: `touch.sent`, `touch.delivered`, `touch.replied`

#### Variant A_speed — speed camera

```
היי {{name}}, איתרנו עבורך דוח חדש ⚠️ איזה באסה.

הפרטים:
• עבירה: דוח מהירות
• סכום: ₪{{fine.amount}}
• רשות: {{fine.authority}}
• תאריך: {{fine.date}}

לפני שאתה רץ לשלם — עצור רגע. דוחות מהירות מתבטלים בכמות לא קטנה בגלל טעויות במכשור, חוסר כיול, או פגמים בתיעוד. המומחים שלנו ב-VIP יודעים בדיוק על מה לערער ברשות הזאת ומכינים את הערעור בשמך.

יש שני מסלולים:
1️⃣ ערעור נקודתי על הדוח הזה — ₪49 חד פעמי. המומחים שלנו מטפלים בדוח הזה, נגמר.
2️⃣ VIP — ₪489/שנה, ערעורים בלתי מוגבלים על כל דוח שיופיע + ספיגת ריבית פיגורים. עדיף אם זה לא הדוח הראשון או האחרון שלך.

איזה כיוון מתאים לך? אני סוכן AI דיגיטלי וכאן לעזור.
```

#### Variant A_parking — parking

```
היי {{name}}, איתרנו עבורך דוח חניה חדש ⚠️ איזה באסה.

הפרטים:
• עבירה: חניה
• סכום: ₪{{fine.amount}}
• רשות: {{fine.authority}}
• תאריך: {{fine.date}}

לפני שמשלמים — דוחות חניה לרוב נופלים על אחד משלושת אלה: סימון לא ברור של הרחוב, חוסר תיעוד מספק של הפקח, או חוסר עמידה בנהלי הרשות. המומחים שלנו מכירים את הנקודות האלו לעומק.

שני מסלולים זמינים:
1️⃣ ערעור נקודתי — ₪49 חד פעמי, מטפלים בדוח הזה בלבד.
2️⃣ VIP — ₪489/שנה, הכל פנימה.

איזה מתאים? אני כאן.
```

#### Variant A_phone — driving while using phone

```
היי {{name}}, איתרנו דוח חדש על שמך — עבירת שימוש בטלפון ⚠️ באסה שלמה.

הפרטים:
• עבירה: שימוש בטלפון בזמן נהיגה
• סכום: ₪{{fine.amount}}
• רשות: {{fine.authority}}
• תאריך: {{fine.date}}

זה לפי החוק הישראלי דוח עם נקודות, וזה גם הסוג של דוח שעובד עליו ערעור היטב — לרוב הקושי של הרשות הוא לזהות חד-משמעית את הנהג ולא רק את הרכב. המומחים שלנו ב-VIP מתמחים בדיוק בנקודה הזאת.

שני מסלולים:
1️⃣ ערעור נקודתי — ₪49 חד פעמי על הדוח הזה.
2️⃣ VIP — ₪489/שנה, הכל פנימה לכל דוח עתידי.

איזה מתאים לסיטואציה שלך?
```

#### Variant A_red_light — running a red light

```
היי {{name}}, איתרנו עבורך דוח חדש — עבירת אור אדום ⚠️ זה דוח רציני.

הפרטים:
• עבירה: אור אדום
• סכום: ₪{{fine.amount}}
• רשות: {{fine.authority}}
• תאריך: {{fine.date}}

זה דוח עם נקודות גבוהות שיכול להוביל ישירות לקורס נהיגה מונעת או פסילה אם תצטרף לדוחות נוספים. המומחים שלנו ב-VIP יודעים לבחון את התיעוד של הצומת — לעיתים יש בעיות בזיהוי הרכב או בתזמון של תיעוד האירוע.

שני מסלולים:
1️⃣ ערעור נקודתי — ₪49 על הדוח הזה.
2️⃣ VIP — ₪489/שנה, הגנה מלאה.

מומלץ לטפל בזה מהר. איזה מתאים?
```

#### Variant A_other — any other / unknown violation

```
היי {{name}}, איתרנו עבורך דוח חדש על שמך ⚠️ איזה באסה.

הפרטים:
• עבירה: {{fine.violation_type}}
• סכום: ₪{{fine.amount}}
• רשות: {{fine.authority}}
• תאריך: {{fine.date}}

לפני שתשלם — שווה לבדוק אם יש עילה לערעור. בהרבה מקרים יש פגמים בנוהל, באכיפה, או בתיעוד שיכולים להוביל לביטול הדוח והנקודות.

שני מסלולים:
1️⃣ ערעור נקודתי — ₪49 חד פעמי.
2️⃣ VIP — ₪489/שנה.

איזה כיוון מתאים?
```

**Quality checklist (touch 1):**
- [x] Empathy in line 1
- [x] Structured fine details (the user can verify it's "their" fine)
- [x] Violation-specific appeal angle (no generic "every fine can be cancelled")
- [x] Dual CTA — one-off + VIP (real choice)
- [x] No invented success rates
- [x] 7 paragraphs (allowed exception for the structured details block)
- [x] AI disclosure in closing line of A_speed variant — confirm consistency across all

---

### Touch 2 — Cost-of-waiting + empathetic re-engage

**Delay**: +24h after touch 1 if no reply
**Variants**: A (single, no violation-type variation here — generic enough)
**Skip conditions**: replied, converted, opted out, escalated, fine already paid (orchestrator checks)
**Exit conditions**: replied → branches | continues to touch 3
**Events emitted**: standard

```
היי {{name}}, רק לוודא — הדוח שאיתרנו ({{fine.violation_type}}, ₪{{fine.amount}}) עדיין פתוח.

זה לא דחיינות שלי, זה זמן ספציפי: אחרי 90 יום מתאריך הדוח, הסכום קופץ ב-50% אוטומטית, וזה לא ניתן להחזרה. אם תרצה לערער — הזמן עכשיו, לא בעוד חודש.

הדרך הכי קצרה לטפל בזה היא או ערעור נקודתי ב-₪49, או לעבור ל-VIP ולסגור את הסיפור על כל דוח עתידי. תרצה שאעבור איתך על האפשרויות?
```

---

### Touch 3 — Final escalation / handoff to C7

**Delay**: +5 days after touch 2 (~6 days from touch 1)
**Variants**: A (single)
**Skip conditions**: standard
**Exit conditions**: after sending → `exhausted` AND emit a `c7.eligible` signal (C7 picks up if its trigger predicate matches; otherwise sequence ends)
**Events emitted**: `touch.sent`, `touch.delivered`, `sequence.exhausted`, optionally `handoff.to.c7`

```
היי {{name}}, פעם אחרונה ממני בנושא הדוח שאיתרנו.

אני מבין שזה לא היה רגע נוח, ואני לא רוצה להציק. רק שתדע: עוד שבועיים-שלושה הדוח עובר לסטטוס של גבייה רשמית והאופציות לערער מצטמצמות בצורה משמעותית.

אם תרצה לדבר — אני כאן. אם לא — נסיעה בטוחה.

({{plan_link}} עדיין זמין.)
```

After this touch + 24h no reply: sequence is `exhausted`. If the user is also eligible for C7 (viewed the fine in-app but didn't convert), C7 fires with the coupon variant on a separate timer.

---

## Branches

### B1 — User confirms they want to handle it ("כן" / "אוקיי" / "תשלח לי")
**Bot reply:**
```
מעולה. רק להבין איך הכי נכון לטפל:
— אם זה דוח חד פעמי שצריך להיסגר ולשכוח ממנו → ערעור נקודתי ב-₪49. הקישור: {{one_off_appeal_link}}
— אם זה לא הראשון או האחרון, ויש סיכוי לעוד דוחות → VIP ב-₪489/שנה. הקישור: {{plan_link}}

איזה תרצה?
```
**Event**: `branch.taken: ready_to_engage`

### B2 — Frustration / venting ("אוף, איזה מעצבן", "באמת אפשר לבטל?")
**Empathy-first gender-aware response.**

**Masculine:**
```
מבין אותך לגמרי, דוח כזה זה הדבר האחרון שצריך על הראש. זה הכי מבאס להרגיש ש'תפסו' אותך באמצע היום.

אבל אל תתייאש — הרבה דוחות מהסוג הזה מתבטלים בגלל פגמים בתיעוד או באכיפה. המומחים שלנו יודעים בדיוק איפה לחפש את הנקודות האלו ולערער. חבל לשלם ₪{{fine.amount}} ולצבור נקודות אם יש סיכוי לבטל.

רוצה שאשלח לך את הפרטים? נתחיל ב-₪49 ערעור נקודתי, או נעבור על VIP אם זה דפוס.
```

**Feminine:**
```
מבין אותך לגמרי, דוח כזה זה הדבר האחרון שצריך על הראש. זה הכי מבאס להרגיש ש'תפסו' אותך באמצע היום.

אבל אל תתייאשי — הרבה דוחות מהסוג הזה מתבטלים בגלל פגמים בתיעוד או באכיפה. המומחים שלנו יודעים בדיוק איפה לחפש את הנקודות האלו ולערער. חבל לשלם ₪{{fine.amount}} ולצבור נקודות אם יש סיכוי לבטל.

רוצה שאשלח לך את הפרטים? נתחיל ב-₪49 ערעור נקודתי, או נעבור על VIP אם זה דפוס.
```

**Event**: `branch.taken: frustration`

### B3 — "I'll just pay it"
Pull from objection library + add real-time context:
```
אם תשלם עכשיו, אתה בעצם מודה בעבירה — והנקודות נרשמות אוטומטית ברישיון. הנקודות נצברות ויכולות להוביל לקורס נהיגה מונעת או פסילה. ערעור מעמיד את הדוח לבדיקה אמיתית — בהרבה מקרים מבטל את הקנס וגם את הנקודות.

₪49 לערעור נקודתי על הדוח הזה — שווה את הניסיון כשהאלטרנטיבה היא ₪{{fine.amount}} + נקודות. רוצה לנסות?
```
**Event**: `branch.taken: pay_anyway`, `objection.raised: pay_anyway`

### B4 — "How does the appeal work?"
Per FAQ:
```
המומחים שלנו מנסחים ערעור מקצועי המבוסס על: סוג העבירה, פרטי האירוע, נסיבות מקלות, ופרצות בנוהל של הרשות הספציפית. את הערעור אתה רואה לפני ההגשה, מאשר, וחותם. ההגשה היא בשמך — אתה הגורם החתום.

תרצה להתחיל? ₪49 לערעור הזה, או VIP אם תרצה כיסוי לעתיד.
```
**Event**: `branch.taken: how_appeal_works`

### B5 — "Are you lawyers?"
Canonical legal-line response per objection library. **Critical not to deviate here** — this is the highest-risk lane.
**Event**: `branch.taken: law_firm`

### B6 — "Who are you?"
```
אני העוזר הדיגיטלי של Road Protect — סוכן AI שמנטר עבורך דוחות בזמן אמת ועוזר לערער עליהם לפני שהם הופכים לכפל קנס. כאן כדי להגן עליך בדרכים. 🛡️
```
**Event**: `branch.taken: identity_check`

### B7 — User says "I already paid it"
```
אם הדוח כבר שולם, לא ניתן להחזיר את הכסף בערעור (התשלום נחשב להודאה בעבירה). אבל — אם תרצה הגנה ל-future, כך שזה לא יקרה שוב, VIP עוצר את כדור השלג. רלוונטי?
```
**Event**: `branch.taken: already_paid`

### B8 — Opt-out
Per § 0.8.

### B9 — Other
Fall to B1 inbound.

---

## Quiet hours behavior (override)

C5 is **real-time**, so quiet hours apply but with a tighter window:
- **Defer to 08:00 next day** if `fine.detected_at` is between 22:00–08:00 (weekday) or during Shabbat.
- **Do not delay further than 12 hours**: if the deferral would push beyond 12h, send at 08:00 even if it's close to quiet hours' edge.

The clock on the user's "appeal window" doesn't care about our quiet hours.

---

## Suppression and exit

- **C5 always wins** over other outbound scenarios (highest priority in matrix).
- **One C5 per fine_id** — even if user has multiple new fines, send one C5 listing the most recent / highest-amount one, mention the others as "+ X more open."
- **Converted via this scenario**: `converted` with `plan ∈ {one_off, vip}` and revenue captured.
- **User pays the fine directly to authority** (detectable via fine.status = 'paid_external'): sequence ends with `expired`, log it for "one we lost to authority" cohort.

---

## Events emitted

Standard + C5-specific:
- `fine.detected` — upstream event that triggers C5 (not the bot's own event, but C5 references it)
- `dual_cta.shown` — every C5 touch 1 shows both one-off and VIP — track which they click via UTM
- `handoff.to.c7` — when sequence exhausts but C7 trigger applies
- `lost_to_authority` — if `fine.status = 'paid_external'` during sequence

---

## A/B testing slots

- **Variants A_speed / parking / phone / red_light / other** — already 5-way; can A/B inside each (e.g., dual-CTA-order: one-off first vs VIP first)
- **Touch 1 with dual CTA vs VIP only** — does adding the ₪49 option boost conversion or cannibalize VIP?
- **Empathy intensity**: "איזה באסה" vs more neutral opener — measure reply rate by emotional register

---

## Open questions for Yossi

1. **One-off (₪49) integration in C5**: the original scenario flagged this as an open question. My spec puts it in. Confirm this is the right call — main risk is cannibalizing VIP conversions. Mitigated by dashboard tracking which CTA each conversion clicked.
2. **What about second-fine on the same user mid-sequence**: if a user is in C5 sequence for fine A and fine B is detected — do we send another C5? My spec: no, augment the next touch's copy with "+ another fine appeared." Confirm.
3. **Real-time delivery latency**: bot must fire within 5 minutes — is that achievable in the new vendor's stack?
4. **Violation type "other"**: if `fine.violation_type` is null or unrecognized, A_other variant runs. Do we want a fallback that *doesn't* claim "many fines of this sort are cancellable" since we don't know what it is?
