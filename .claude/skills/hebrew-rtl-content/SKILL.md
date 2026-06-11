---
name: hebrew-rtl-content
description: Use when writing or editing Hebrew marketing copy, landing pages, ads, emails, or any user-facing text for Road Protect — anything in 07_marketing/copy/ or any Hebrew text-heavy deliverable. Trigger phrases include "write a Hebrew [email/ad/landing/headline]", "draft copy", "כתוב לי", "תרגם ל-Hebrew with the brand voice", "RTL HTML for…". Keeps the brand voice consistent with the existing bot scenarios and respects the legal disclaimer.
---

# Hebrew RTL Content Skill for Road Protect

How to write Hebrew copy that sounds like Road Protect, not like a translation engine.

## Voice in one sentence

Warm, practical, occasionally cheeky Israeli friend who happens to be very good at handling traffic-fine bureaucracy.

## Hard rules

1. **Hebrew text is right-to-left.** In HTML, always wrap the content in `<html dir="rtl" lang="he">` or use `<div dir="rtl">` for scoped sections.
2. **Mixed-language tokens** ("Road Protect", "VIP", "WhatsApp") stay in Latin script. Don't transliterate them.
3. **Numerals** are LTR even inside RTL Hebrew. "₪489 לשנה" — the ₪ sits before the digits, the rest reads right-to-left.
4. **Quote marks** in Hebrew are `״` (gershayim) for full quotes, or just regular `"`. Don't use English curly quotes.
5. **Voice register** is mostly informal-direct, slightly warm. Never *formal-bureaucratic* (sounds like a government form) and never *over-casual* (sounds like a teenager).

## Vocabulary — words we use vs. words we don't

| Use this | Not this | Why |
|---|---|---|
| מומחים, צוות מומחים | עורכי דין | Legal line — we're not a law firm |
| מערכת חכמה, רדאר | אלגוריתם | More approachable |
| ביטול דוח, ערעור על דוח | "לוחמה משפטית" | Don't overclaim |
| שקט נפשי | רוגע, פיס אוף מיינד | Authentic phrase |
| כפל קנס, ריבית פיגורים | "תוספות", "עמלות" | The specific terms drivers know |
| נהיגה בראש שקט | "חוויית נהיגה" | Simpler is better |
| איזה באסה, חבל סתם | "מאוד מצטערים על אי הנעימות" | Real Israeli register |

## Sentence structure

- **Short sentences.** Two clauses per sentence is the upper end.
- **Open with the user's reality**, not with the brand. "קיבלת דוח? אנחנו כאן" not "Road Protect is the leading platform for…"
- **End paragraphs with a hook** — a question, a stat, or a punchy promise.

## Headlines — the formula that works

The existing site uses formulations like:

- "סורקים עבורך קנסות אבודים מול כלל הרשויות" (verb + benefit + scope)
- "השקט שלך מתחיל כאן" (possessive + emotional state + place)
- "ההגנה שלך בדרכים" (possessive + product role)

Stay in this lane. Avoid:
- "מובילים בתחום" (leader-claims without proof)
- "המהפכה החדשה ב-" (overhyped)
- "כל מה שתמיד רצית" (filler)

## CTAs

What works in the Road Protect surface:

- "תבדקו עבורי עכשיו" (defer the work: "check for me")
- "הגש ערעור" (action)
- "שדרג למסלול VIP" (action + plan name)
- "אשמח לפרטים" (low-friction conversational trigger)

What doesn't:

- "לחץ כאן" (generic, dead)
- "התחל עכשיו!" (over-pushed)
- "Get started" code-switched (off-brand)

## Numbers and stats — how to use

The brand leans heavily on stats:

- ₪2,150 — average driver fine spend over 3 years
- 50% — late-payment interest surcharge
- 10M+ — fines issued in Israel per year
- 29% — YoY increase in enforcement
- 30,000 — drivers protected (marketing claim)

Use them as **cold splashes** — short, isolated, impossible to argue with. Don't pad with context unless you have a stat that *demands* explanation.

## The legal line in copy

Anything implying lawyer representation = stop, rewrite. See `/01_business_context/LEGAL_DISCLAIMER.md`.

Safe phrasings:
- "מומחים שמלווים אותך בערעור"
- "ניסוח מקצועי של בקשת הערעור"
- "הצוות שלנו עוזר לך לערער"

Forbidden:
- "עורכי הדין שלנו"
- "ייצוג משפטי"
- "מבטיחים ביטול"

## Common deliverable structures

### Landing-page hero section
```
[headline — 6-10 words, benefit-led]
[subhead — 1 sentence, expanding the benefit]
[CTA button — verb + outcome]
[social proof line — 1 short line]
```

### WhatsApp/SMS message
```
[Greeting + name, when known]
[The reason for contact / the situation]
[The proposed action or info]
[Soft CTA / question]
```
Max ~6 short paragraphs. Line breaks generously.

### Email subject lines
- Question form: "קיבלת דוח? אל תרוץ לשלם"
- News form: "רפורמת התעבורה 2026 — מה הלאה"
- Account form: "שנת ההגנה שלך מסתיימת בעוד 30 יום"

Avoid: ALL CAPS, exclamation chains, "פתח עכשיו!!!"

## Translation guidance (English → Hebrew)

When asked to translate marketing copy from English:

1. Don't translate word-for-word. Translate the *intent*.
2. Match register — startup-warm in English → startup-warm in Hebrew, not bureaucratic Hebrew.
3. Length differs — Hebrew is often more compact than English. Don't pad to match.
4. Brand names (Road Protect, VIP, Detection) stay in Latin if that's how they appear in product. Plan names ("מסלול VIP", "מסלול איתור") use Hebrew with the brand term in Latin.

## RTL in HTML mockups

```html
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>...</title>
  <!-- Use a Hebrew-supporting font: Rubik, Heebo, Assistant, or system fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>body { font-family: 'Rubik', sans-serif; }</style>
</head>
<body class="bg-white text-gray-900">
  <!-- content here, in Hebrew, with Tailwind RTL classes -->
</body>
</html>
```

When using Tailwind:
- `mr-` and `ml-` *flip* under RTL, so use them spatially as if on an LTR canvas — Tailwind handles the flip via the `dir` attribute.
- Or use logical properties: `ps-` (padding-start), `pe-` (padding-end), `ms-`, `me-`.

## Brand colors (extracted from the live site)

- **Primary navy / dark blue** — the shield logo color. Roughly `#1a3a5c` to `#0e2540`. Use for primary CTAs, headers.
- **White background** for most surfaces.
- **Warning / fine alert** — red/orange (`#dc2626`, `#ea580c`) for "fine detected" states.
- **Success** — green (`#10b981`) for "protected", "appeal won".

Confirm exact values from the live site when building production assets.
