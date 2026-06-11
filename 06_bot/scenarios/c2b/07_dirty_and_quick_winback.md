# C7 — "Dirty & Quick" Winback (Abandoned Appeal)

**Channel**: WhatsApp (C2B agent, outbound)
**Audience**: Users who **started a single appeal in our system and abandoned it before payment** (status = `basic_details` / `violation_details`)
**Goal**: Get them to **complete the appeal they started** with a 30% coupon. NOT a VIP pitch — that comes later, after they've experienced the system end-to-end.
**Tone**: Direct, slightly urgent, transactional. The "dirty" implies fast and pragmatic — not deceptive.

## Trigger

User started the appeal flow (status = `basic_details` or `violation_details`) and did not complete checkout within [X] hours → fires.

> These are the smartest leads we have (per Yossi, even hotter than Trademobile): they have a fine in hand, started a process, and dropped. This must be a **proactive** bot message.

## Variables

- `{{name}}`
- `{{coupon_code}}` — `SAVE30` (the only code; there is no 50% / no "choose your discount")

## Opening message

```
היי {{name}}, כאן צוות Road Protect 🛡️

ראינו שהתחלת אצלנו תהליך ערעור על דוח אבל לא סיימת אותו. חבל להשאיר את זה פתוח — דוח שלא מטופל בזמן צובר ריבית פיגורים של 50% ועלול להמשיך ולהסתבך.

כדי לעזור לך לסגור את זה, סידרנו לך 30% הנחה על הערעור הנוכחי. המומחים שלנו ייקחו מכאן את הטיפול וילחמו למקסם את סיכויי ביטול הדוח והנקודות עבורך.

קוד הקופון שלך לערעור הזה: {{coupon_code}}

רוצה לסיים את הערעור עכשיו? כל מה שנשאר זה להשלים את התהליך כאן: [לינק להמשך הערעור]
```

> ⚠️ Say "תהליך הערעור שהתחלת" — **not** "הדוח שאיתרנו לך". These users brought their own fine into the appeal flow; we didn't necessarily detect it on radar. Claiming we "detected" a fine the user found themselves reads as surveillance and creates confusion (Yossi, 28/04).

## Branches

### B1 — "Why appeal and not just pay the fine?"
```
אם תשלם את הדוח עכשיו, אתה בעצם מודה בעבירה וסופג את הנקודות. הנקודות נרשמות לך ברישיון ויכולות להוביל מהר מאוד לקורסי נהיגה מונעת או אפילו לפסילה אם יצטברו עוד בעתיד.

מעבר לזה, אם תשלם באיחור אפילו של יום, הקנס יקפוץ אוטומטית ב-50% בגלל ריבית פיגורים.

המומחים שלנו מגישים ערעור מקצועי בשמך כדי לנסות לבטל את הדוח ואת הנקודות. עם 30% ההנחה זה יוצא ממש זול יחסית למה שדוח לא מטופל יכול לעלות לך. חבל לשלם למדינה סתם אם אפשר לנסות לבטל, לא?
```

### B2 — "How do I use the coupon?"
```
פשוט מאוד! כנס/י ללינק ששלחתי כאן למטה, ובמעמד התשלום יהיה לך מקום להזין את הקוד {{coupon_code}}. המחיר יתעדכן אוטומטית עם 30% הנחה על הערעור.

ברגע שתסיים/י, המומחים שלנו מקבלים את כל הפרטים של הדוח ומתחילים לעבוד עליו מיד. אני כאן אם צריך עוד משהו 🛡️
```

## After they convert — gradual upsell (not in this message)

Conversion must be **gradual** (Yossi, 30/04). A user who wouldn't pay for one appeal won't jump straight to an annual subscription. The job of *this* flow is only to close the abandoned appeal. Once they've completed it and experienced the system end-to-end, a **separate, later** flow offers VIP. Don't cram a subscription pitch into the abandoned-appeal message.

## Coupon strategy notes

- The coupon is **30%, one code (`SAVE30`), on the single appeal (₪49)** — never on VIP.
- **No 50% code.** We never agreed on 50% (Yossi, 28/04). Don't offer a choice between discounts inside a message — one coupon, one clear goal.
- **The discount applies to the *current* appeal** — say so explicitly. The bot previously failed to clarify this and it confused users (Yossi, 30/04).
- Cold leads and no-fine cohorts get **no coupon** — VIP is already low-priced and we don't want to train the audience to wait for discounts.

## Risk

This is the most "salesy" of the flows. Audit periodically:
- Are users converting after the coupon, or are we training the audience to wait for discounts?
- Is there a complaint signal? (Users feeling pressured / surveilled.)
- Are we keeping the message focused on the appeal and not drifting into a premature VIP pitch?

## Open questions

- Cart-abandon trigger — what's the exact time/status threshold that fires this message?
- Once an appeal is completed via this flow, how long do we wait before the VIP upsell flow fires?
