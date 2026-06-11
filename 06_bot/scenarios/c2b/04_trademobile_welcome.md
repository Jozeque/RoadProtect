# C4 — Trademobile Welcome (New Car Buyer)

**Channel**: WhatsApp (C2B agent, outbound)
**Audience**: New Trademobile customer who just bought a car (= just enrolled in 1 year free Detection)
**Goal**: Welcome, establish the value of "protected in advance," set the stage for later VIP upsell
**Tone**: Celebratory, informative, no hard sell

## Trigger

Trademobile car purchase event → Road Protect account created → welcome message fires within 24h.

## Variables

- `{{name}}` — from `$('Edit Fields').item.json.name`

## Opening message

```
היי {{name}}, כאן צוות Road Protect, ברכות על הרכב החדש! 🚗

רצינו לעדכן שעם רכישת הרכב ב-טרייד מוביל, חבילת התראות וניטור דוחות לשנה שלמה כבר מחכה לך אצלנו — ללא עלות.

למה זה כל כך חשוב? היום, עם רפורמות התעבורה והעומס הבירוקרטי, דוחות רבים פשוט "הולכים לאיבוד" בדואר ולא מגיעים לידיים של הנהגים בזמן. התוצאה היא בדרך כלל כפל קנס, צבירת נקודות והליכי גבייה מעיקים — פשוט כי לא הייתה ידיעה על קיום הדוח.

כאן אנחנו נכנסים לתמונה: המערכת שלנו מנטרת את מאגרי הרשויות ברקע ושולחת התראה בזמן אמת ברגע שנרשם דוח חדש על שמך. המטרה היא להעניק לך שקט נפשי ולחסוך התעסקות עם רגולציות ובירוקרטיה מיותרת.

אנחנו כאן כדי לשמור על הרישיון והכיס שלך בדרכים! 🛡️

יש לך שאלה על השירות או על דוח שהתקבל? אני סוכן ה-AI של Road Protect ואפשר לשאול אותי כאן הכל ✨
```

## Alternative opening (the "step 1 of the example trade-mobile flow" — softer)

```
בוקר אור! איזה כיף שהצטרפת ל-Road Protect, מזל טוב על הרכב החדש! 🚗

מהיום אפשר לנהוג בראש שקט כי המערכת כבר סורקת עבורך הכל. ברגע שיעלה קנס על שמך, הודעה נוחה תגיע מיד לוואטסאפ ולמייל.

חשוב לדעת שרוב הנהגים עושים טעות ומתעלמים מדוחות עד שזה מאוחר מדי. דוח שלא מטופל בזמן גורר ריבית פיגורים של 50% וכפל קנס שיכול להגיע לאלפי שקלים. במסלול ה-VIP שלנו המומחים נלחמים בשבילך כדי שלא נגיע למצב הזה והרישיון יישאר נקי.

רוצה לשמוע איך אנחנו דואגים שלא יתבזבז לך שקל מיותר?
```

The first variant is the "official" welcome (clean, no upsell in the first message). The second variant front-loads the VIP. **Default to variant 1** for the welcome moment and let later flows do the selling.

## Gender detection

The agent should detect gender from the user's first reply and adjust pronouns for all subsequent messages:

- Masculine cues: "אני מעוניין", "מעניין אותי", "אני רוצה לדעת"
- Feminine cues: "אני מעוניינת", "מעניין אותי" + other context, names typically female

Once detected, lock the gender for the conversation.

## Branches (when user replies)

### B1 — "What does VIP cost?" / "Tell me more"
→ Variant 2 logic, but explanation comes from the bot voice. Lead with the cost of inaction (50% interest, double-fine, points), then position VIP as insurance.

### B2 — "What's כפל קנס?" / "What's ריבית פיגורים?" (clarification questions)
→ Plain-language answer. See `../knowledge_base/faq.md` for the canonical definitions.

### B3 — "I'm not interested" / "Just leave it on"
→ Gracious: "אין בעיה, אני כאן אם תשתנה דעתך." Don't push. The free year is doing the work — they'll see the value when a fine pops.

## Open questions for Yossi

- Is the welcome message sent immediately or is there a delay (e.g. 24h after purchase, when the buzz fades)?
- Do we have data on which variant performs better (clean welcome vs. front-loaded sell)?
- Should there be a "month 1 check-in" 30 days post-welcome with stats ("we scanned X databases for you this month")?
