# C5 — Free-Tier User Just Got a Fine

**Channel**: WhatsApp (C2B agent, outbound, near-real-time)
**Audience**: User on Detection plan (or Trademobile free year) where the radar just flagged a new fine
**Goal**: Empathy → urgency → push to VIP for appeal handling
**Tone**: Empathetic first ("איזה באסה"), then strategic

## Trigger

Real-time fine detected → user not on VIP → message fires within minutes.

## Variables

- `{{name}}`
- `{{fine_details}}` — type, amount, authority, date (rendered as a separate block)

## Opening message

```
היי {{name}}, כאן צוות Road Protect 🛡️ איתרנו עבורך דוח חדש ⚠️ איזה באסה!

שלחנו לך עכשיו את פרטי הדוח בצורה נגישה למייל.

[פרטי הדוח]

רגע לפני שרצים לשלם — שווה לעצור. במסלול ה-VIP המומחים שלנו נכנסים לתמונה, מגישים את הערעור בשמך ונלחמים כדי שלא ישולם שקל מיותר.

דוח שלא מטופל בזמן צובר ריבית פיגורים של 50%, ואם מצטברים עוד דוחות זה יכול להגיע גם לכפל קנס. חבל לשלם סתם אם אפשר לערער, נכון?

רוצה לשמוע איך אנחנו ממקסמים את סיכויי הביטול עבורך? אפשר כאן: [לינק לדף נחיתה] או פשוט לכתוב לי 'אשמח לפרטים' ונדבר.
```

## User responds in frustration

Typical reply: "אוף, איזה מעצבן זה. קיבלתי על מהירות וזה 750 שקל. אין לי כוח לזה עכשיו, באמת אפשר לבטל דבר כזה?"

## Empathy-first response (gender-aware)

**Masculine:**
```
מבין אותך לגמרי, דוח כזה זה באמת הדבר האחרון שצריך על הראש. זה הכי מבאס בעולם להרגיש שסתם 'תפסו' אותך.

אבל אל תתייאש, המון דוחות מהירות מתבטלים בגלל טעויות טכניות או חוסר דיוק במכשור. המומחים שלנו ב-VIP יודעים בדיוק איפה לחפש את החורים האלו בדוח כדי להוציא אותך מזה בלי לשלם ובלי לצבור נקודות שיכולות לסבך לך את הרישיון בהמשך.

חבל לשלם 750 שקל ולקבל נקודות אם אפשר לערער. רוצה שאשלח לך את הפרטים ונתחיל לטפל בזה?
```

**Feminine:**
```
שמעי, אני מבינה אותך לגמרי, דוח כזה זה באמת הדבר האחרון שצריך על הראש. זה הכי מבאס בעולם להרגיש שסתם 'תפסו' אותך באמצע היום.

אבל אל תתייאשי, המון דוחות מהירות מתבטלים בגלל טעויות טכניות או חוסר דיוק במכשור. המומחים שלנו ב-VIP יודעים בדיוק איפה לחפש את החורים האלו בדוח כדי להוציא אותך מזה בלי לשלם ובלי לצבור נקודות שיכולות לסבך לך את הרישיון בהמשך.

חבל לשלם 750 שקל ולקבל נקודות אם אפשר לערער. רוצה שאשלח לך את הפרטים ונתחיל לטפל בזה?
```

## "Who are you?" branch

```
אני העוזר הדיגיטלי של Road Protect, כאן כדי להגן עליך בדרכים. המטרה שלי היא לוודא שלא תשלם/י סתם קנסות וריביות פיגורים של 50% בגלל דברים שאפשר לבטל. אני כאן כדי לעזור לך לעבור את הבאסה הזאת הכי בקלות שאפשר. 🙂
```

## Things to be careful about

- **Open with brand identity.** A user who just got a fine alert often thinks it's from the municipality. Lead with "כאן צוות Road Protect" so they know who's writing (Yossi, 30/04).
- **Don't claim guaranteed cancellation.** Use "ממקסמים את סיכויי הביטול" / "המון דוחות מתבטלים" — not "נבטל לך את הדוח" or "דואגים לביטול." Emphasize that we fight for the customer and handle the bureaucracy (Yossi, 25/04).
- **Get the כפל קנס mechanic right.** Doubling is driven by repeat fines (per the FAQ, from the 4th fine in 3 years), not by a "3-month timer." For the immediate-urgency hook use ריבית פיגורים (50% once past the payment date); mention כפל קנס as what accumulating fines can lead to.
- **Don't say "lawyers."** "מומחים" is the right word.
- **Match the violation type to the right hook.** Speed-camera = "טעויות טכניות במכשור." Parking = "אי-עמידה בכללי הרשות / חוסר תיעוד." Phone = "ספק זיהוי הנהג." Don't generically claim every fine can be canceled the same way.

## Open questions

- Is the message timing optimal (within minutes of detection)? Or does a 1–2 hour delay convert better (gives the user time to absorb)?
- Should we attach the actual fine PDF/screenshot in WhatsApp, or just link to the in-app view?
- One-off appeal (₪49) as a lower-friction alternative to VIP at this moment — currently not offered in this scenario. Worth testing.
