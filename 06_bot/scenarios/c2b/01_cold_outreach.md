# C1 — Cold Outreach (לא מנויים בכלל)

**Channel**: WhatsApp (C2B agent, outbound)
**Audience**: Leads who left details previously but never subscribed
**Goal**: Re-introduce the product, soft pitch, open a conversation
**Tone**: Warm, informative, low-pressure

## Trigger

User exists in DB with submitted contact details, no active subscription, last touchpoint > [X] days ago.

## Variables

- `{{firstName}}` — from JSON: `$json.user.firstName.item`

## Opening message

```
היי {{firstName}}, כאן Road Protect, ההגנה שלך בדרכים!

אנחנו פונים אלייך כי השארת אצלנו פרטים בעבר לגבי בדיקת דוחות, ורצינו לוודא שלא פספסת את מה שהשקנו.

היום כבר ממש לא חייבים לשלם דוחות "על עיוור". פיתחנו מערכת שמשלבת עורך דין AI יחד עם צוות מומחים, כדי לעשות לך סדר בכל הקנסות והרגולציות שמסבכות נהגים.

המערכת שלנו סורקת עבורך קנסות אבודים מול כלל הרשויות והעיריות בישראל ודואגת שלא יהיו לך הפתעות! המטרה שלנו היא לתת לך שקט נפשי מול הבירוקרטיה ולשמור לך על הכיס.

אשמח לענות לך על כל שאלה — האם יש דוח שנוכל לעזור לך איתו? תרצה לשמוע על השירות שלנו? אני סוכן AI דיגיטלי ואפשר לשאול אותי כל שאלה 🛡️
```

## Branches

### B1 — User asks about a specific fine
→ **Don't collect fine details in this chat** — they'll re-enter them in the appeal flow, and typing the same info twice across two WhatsApp conversations burns them out (Yossi, 25/04).
→ Route to the appeals department: "אל תשלם/י לפני שתבדוק/י! שלח/י 'היי' למחלקת הערעורים שלנו והמומחים ימקסמו את סיכויי ביטול הקנס והנקודות עבורך: [לינק לוואטסאפ ערעורים]" (appeals: 052-586-6982).
→ One-off appeal (₪49) is the natural entry point; the VIP upsell comes later, after they've experienced an appeal end-to-end.

### B2 — User asks "how much does it cost"
→ Defer pricing slightly. Question back: "האם יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא הגנה כללית לעתיד?"
→ Then surface the right plan.

### B3 — User pushes back ("not interested" / "I don't need this")
→ Single light follow-up: the statistic ("נהג ממוצע מקבל לפחות 2 קנסות ב-2026"). Then disengage gracefully and leave the door open.

### B4 — User asks "who are you"
→ "אני העוזר הדיגיטלי של Road Protect, כאן כדי להגן עליך בדרכים."

## Out of scope (don't say in this scenario)

- No coupon — this is cold, not winback.
- No urgency about a specific fine (we don't know they have one).
- No "your free year is ending" framing.

## Success signals to track

- Reply rate (any reply within 72h)
- "Tell me more" / pricing-question rate
- Conversion to one-off or subscription within 14 days

## Open questions for Yossi

- What's the current reply rate baseline?
- Are we filtering by recency of original lead, or blasting the whole back-catalog?
- Is there a frequency cap? (No more than 1 cold message per N months per lead.)
