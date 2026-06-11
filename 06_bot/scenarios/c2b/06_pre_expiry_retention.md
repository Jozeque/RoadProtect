# C6 — Pre-Expiry Retention (30 days before free-year ends)

**Channel**: WhatsApp (C2B agent, outbound)
**Audience**: Detection / Trademobile-free-year users 30 days from expiry
**Goal**: Convert to paid before protection lapses; use FOMO + proof-of-value
**Tone**: "Look how much we've done for you — don't lose it"

## Trigger

Subscription expires in 30 days → fires message → optional second touch at 14 days, 3 days, day-of.

## Variables

- `{{name}}`
- `{{events_count}}` — number of fines detected / scans run during the year

## Opening message

```
היי {{name}}, שים לב — שנת ההגנה שלך ללא עלות עומדת להסתיים בעוד 30 יום. במהלך השנה הזו שמרנו עליך וניטרנו עבורך {{events_count}} אירועים/בדיקות.

לנהוג בלי Road Protect זה כמו לנהוג בלי ביטוח — ברגע שמקבלים את ההודעה מהמשטרה, זה כבר מאוחר מדי.

שדרג עכשיו למסלול ה-VIP שלנו כדי לשמור על רישיון נקי ושקט נפשי.
```

**CTA**: שמור על השקט הנפשי שלך גם בשנה הבאה. הבטח את מקומך ב-VIP שלנו כאן: [לינק לדף נחיתה לסליקה]

## Branches

### B1 — "What's the difference between what I have now and VIP?"
```
שאלה מצוינת. עד עכשיו היית במסלול האיתור — זה אומר שסרקנו עבורך את המאגרים ושלחנו התראות לוואטסאפ ולמייל ברגע שצץ דוח. זה נותן שקט, אבל אם באמת מגיע דוח, האחריות לטפל בו היא עליך.

במסלול ה-VIP אנחנו לוקחים את זה צעד קדימה. המומחים שלנו נכנסים לזירה במקומך, מגישים את הערעורים ונלחמים כדי לבטל את הקנס והנקודות. במקום שתיפול על ריבית פיגורים של 50%, אנחנו דואגים לסגור את הסיפור. זה בעצם המעבר מ'לדעת שיש בעיה' ל'לפתור את הבעיה'.
```

### B2 — "I didn't get any fines this year, why pay?"
```
הלוואי וגם השנה הבאה תעבור בלי אף דוח! אבל בוא נודה על האמת — הכבישים היום מלאים במצלמות חדשות ובאכיפה מוגברת. מספיק רגע אחד של חוסר תשומת לב או טעות טכנית של שוטר, ופתאום מגיע קנס של אלפי שקלים עם נקודות שחונקות את הרישיון.

ה-VIP הוא רשת הביטחון שלך. דוח אחד שמתבטל מחזיר לך את עלות המינוי לכמה שנים קדימה, ומונע ממך להיכנס לסחרור של כפל קנס וקורסי נהיגה מונעת. חבל לוותר על ההגנה הזאת בדיוק כשאתה כבר רשום במערכת, לא?
```

### B3 — "Do you actually cancel fines? Or is this just 'peace of mind'?"
```
אנחנו לא רק 'בשביל השקט'. המומחים שלנו מכירים את כל הפרצות והנהלים של המשטרה והרשויות. הם יודעים בדיוק על מה לערער כדי להמיר דוח באזהרה או לבטל אותו לחלוטין.

המטרה שלנו היא אחת: לחסוך לך את הכסף ואת הנקודות. במקום שתשלם למדינה קנס מנופח, אתה מקבל גב מקצועי שנלחם בשבילך. רוצה לראות איך אנחנו הופכים את האיתות לביטול דוח בפועל? הנה כל הפרטים: [לינק לדף נחיתה]
```

## Improvements to consider

1. **Replace `{{events_count}}` with richer data** when available — fines detected, ₪ saved, alerts sent, time-to-alert vs. official letter.
2. **A/B test the FOMO framing vs. a value-recap framing**: "We scanned X databases / Y times for you" might convert better than "your protection is ending."
3. **Add a coupon for users who don't convert at 30 days** — escalates into C7 (Dirty & Quick) at 14 or 7 days.

## Open questions

- Touch cadence: 30 / 14 / 3 / 0 days, or is this too aggressive?
- Channel mix — pair WhatsApp with email for users who don't reply?
- Personalized year-in-review (e.g. "we scanned 142,000 records for you and found 2 fines") — needs build effort, likely high impact. → Idea candidate.
