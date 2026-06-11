# C2 — Trademobile Active Cohort with Detected Fines

**Channel**: WhatsApp (C2B agent, outbound)
**Audience**: Trademobile users currently on the free Detection year, with ≥1 fine detected
**Goal**: Convert from free Detection to paid VIP
**Tone**: Service-led; "we're already protecting you, here's the next layer"

## Trigger

Trademobile-cohort user, within free year, system has detected ≥2 fines (per the existing template logic).

## Variables

- `{{name}}` — from `$json.name`
- `{{fines}}` — from `$('Edit Fields').item.json.fines` (count of fines detected)

## Opening message

```
היי {{name}}, כאן צוות Road Protect 🛡️

עם רכישת הרכב בטרייד מוביל קיבלת מאיתנו שנת ניטור והתראות במתנה, ובתקופה הזו המערכת שלנו איתרה עבורך {{fines}} דוחות — חשוב לנו לוודא שהם לא נשארים ללא טיפול.

כדי למצות את הזכויות שלך ולחסוך בנקודות וכספים מיותרים, נשמח לשדרג אותך למסלול המלא שלנו. שם נעניק לך ליווי מקצועי מקצה לקצה וטיפול בירוקרטי מלא בכל דוח שאותר.

מעניין אותך לשמוע על היתרונות של המסלול המלא והשקט שהוא ייתן לך? אני סוכן AI דיגיטלי ואפשר לשאול אותי כל שאלה 🛡️
```

> ⚠️ **Trademobile = car purchase, never leasing.** Never say "חברת ליסינג" — Trademobile customers *bought* a car. Always reference "טרייד מוביל" by name and frame the free year as "השירות שקיבלת מטרייד מוביל." The bot identifies Trademobile users from the CRM source field; this reference is mandatory for this cohort (Uri, 26–27/04).

## Branches

### B1 — User asks what VIP includes
→ Three concrete differentiators:
1. ערעורים בלתי מוגבלים על ידי המומחים שלנו
2. ספיגת ריבית הפיגורים (50%) במקרה שהיא נצברת בזמן הטיפול
3. תשלומים ישירות מול העיריות + הפניה לעו"ד מומחה לפי הצורך
→ End with link to plans page.

### B2 — User says "I'll just pay the fine"
→ Cost framing: "אם תשלם עכשיו אתה בעצם מודה בעבירה וסופג את הנקודות. הנקודות נשארות ברישיון ומצטברות."
→ Bridge to VIP: appeal cancels the fine *and* the points.

### B3 — Price objection
→ Math: one cancelled fine of ₪750 covers >1.5 years of VIP. Reframe as insurance, not service.

## Distinction from C3

Different audience, and the opening now **diverges** (it used to be an identical template): C2 is a **Trademobile** user *still in the free year*, so the message explicitly references the Trademobile-gifted free year (mandatory per Uri's feedback). C3 is a general post-expiry lapsed user — dormant account, no Trademobile framing, re-establish first.

## Open questions for Yossi

- Are we segmenting by fine count? (e.g. 1 fine = different message than 3+ fines)
- Is there a "detected fines but user hasn't viewed them in the app" signal that should change the message?
- Conversion rate from this scenario specifically — needs tracking.
