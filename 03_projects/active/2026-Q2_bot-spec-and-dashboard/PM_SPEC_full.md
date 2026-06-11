# Road Protect — WhatsApp Bot & Tracking Dashboard
## Full PM Spec (non-technical, with complete scenario texts)

*The plain-language, product-level view of the whole thing: what we're building, why, who it's for, how each conversation works word-for-word, and what we want to see on the dashboard. The Hebrew copy below is the actual bot text. The build-ready technical detail (trigger predicates, event schemas, suppression logic) lives in `bot-spec/` and `dashboard-spec/` — this doc is the "what & why & what it says."*

**Status:** specing (Q2 2026) · **Owner:** Yossi · **Target:** spec frozen end of Q2, build Q3

---

## 1. What this is, in one paragraph

Road Protect runs two WhatsApp agents and needs one dashboard to run them well. The **outbound agent** reaches out to a driver at a specific moment in their life with us — they just bought a car, a fine just landed, their free year is ending, they started an appeal and stopped. The **inbound agent** answers anyone who messages our WhatsApp number first and routes them to the right place. The **dashboard** is how we see, at a glance, whether all of that is actually working: who we reached, who replied, who paid, and where it broke. This document is the complete definition of both — every scenario, every message, every screen — i.e. exactly what needs to be built.

---

## 2. Why we're doing this

Two needs, and they compound each other.

**The bot has to be unambiguous.** Every scenario must define exactly *who* gets messaged, *when* the follow-up fires, *when* the bot shuts up, and *what* counts as "this person is unhappy." The vague parts are exactly the parts that decide whether the bot feels like a sharp teammate or like spam — so this spec pins all of them down.

**We're blind at the macro level.** Right now we can read individual WhatsApp chats one at a time, but we can't answer the question that actually matters: *"Of everyone we messaged this week, how many replied, how many bought, and where did it fall apart?"* Without that, we can't improve the copy, can't price-test the coupon, and can't justify turning the volume up.

The two feed each other: without the dashboard we can't tell whether a scenario is working, and without clean scenarios the dashboard's funnel has nothing solid to measure.

---

## 3. The value proposition — what "good" looks like

**For the driver:** a bot that feels like a sharp human teammate. It knows who you are, talks to you correctly (your name, your gender, your real fine count, the partner you actually came through), creates genuine urgency without lying, never promises what it can't deliver, and always knows the next right step. That's what turns a cold WhatsApp message into a paying customer — and what makes a paying customer feel looked after instead of marketed at.

**For Road Protect:** a bot we can actually *run* — tune the copy, test the coupon, point volume at the audience that converts — because for the first time we can see the whole funnel instead of guessing from vibes.

---

## 4. The product, part one — the bots

### 4.1 Two bots, one personality

There are two agents but they are the **same AI**: same voice, same rules, same knowledge base. The only difference is who starts the conversation.

- **Outbound ("we reach out first")** — 7 scenarios, C1–C7. Each one fires at a specific life-moment, as a sequence of 1–4 messages ("touches") with deliberate timing between them.
- **Inbound ("they message us first")** — 1 entry flow, B1, that figures out what the person wants and routes them.

### 4.2 The golden rules (true in every single conversation)

These are the bot's personality. They never bend per scenario:

1. **Say who we are, up front.** *"כאן צוות Road Protect."* People who get a fine alert often think it's the municipality — kill that confusion in the first line.
2. **Empathy → urgency → sale.** Acknowledge the annoyance (*"איזה באסה"*) before pitching anything.
3. **One clear ask per message,** and end on a question so the conversation keeps moving.
4. **Gender-neutral until we know.** Start neutral (*"עבורך / שלך"*); once the first reply reveals gender, mirror it. Never guess a name or gender.
5. **The legal line — we are NOT a law firm.** Allowed: *"מומחים"*, *"נלחמים בשבילך"*, *"מנסחים את הערעור בשמך"*. Never: *"עורכי דין שייצגו אותך"*, *"מבטיחים ביטול"*. We maximize the *chances* of cancellation — we never promise it.
6. **Admit we're an AI when asked.** *"אני סוכן AI דיגיטלי."* Never pretend to be a person, never use a human name.
7. **One coupon, one purpose** (see below).
8. **Trademobile = a car purchase, never "leasing."** Name the partner; frame the free year as *"השירות שקיבלת מטרייד מוביל."* In any Trademobile scenario (C2, C4), **message 1 must state up front that we're reaching out *because* of that purchase** — it's why we have their details and the basis for the free year. This grounds the outreach legitimately (same role the "you left details with us" line plays in C1).
9. **Appeals go to the appeals desk.** When someone wants to appeal, send them straight to the appeals WhatsApp (052-586-6982) — don't re-collect fine details in the sales chat, or they'll type it twice and give up.

### 4.3 The one coupon rule

One code: **SAVE30 = 30% off a single appeal (₪49).** It goes out **only** to people who started an appeal and didn't finish (scenario C7). **Never** on VIP, **never** 50%, **never** "pick your discount." The strategy is *gradual conversion*: close the cheap appeal first so they experience the system, then offer VIP later in a separate conversation. Cold leads and people with no fines get **no coupon** — VIP is already cheap, and we don't train people to wait for a discount.

### 4.4 How to read the scenarios below

Each scenario lists: **who it's for**, **the goal**, **the tone**, then **every message the bot sends** (touch by touch, with the gender/fine-count variants where they exist), and the **key reply branches** — what the bot says back when the person responds. The Hebrew blocks are the literal copy. `{{name}}`, `{{fines_count}}`, `{{fine.amount}}` etc. are filled in live from the CRM (see §7).

---

## 5. The 7 outbound scenarios — full texts

### C1 — Cold outreach

- **Who:** old leads who left details but never subscribed (private / ad, not partners).
- **Goal:** re-introduce Road Protect, softly find out if they have a fine right now, open a real conversation.
- **Tone:** warm, informative, low-pressure. They don't remember us — don't act like old friends. Discloses it's an AI in the first message. **No coupon.**

**Touch 1 — Reintroduction + soft diagnostic** (fires immediately). *Variant A, default:*

```
היי {{name}}, כאן Road Protect — שירות ההגנה על נהגים בדרכים.

אני פונה כי השארת אצלנו פרטים בעבר, ורציתי לוודא שלא פיספסת מה שבנינו בזמן האחרון. אני סוכן AI דיגיטלי, ואני כאן לענות על כל שאלה.

המערכת שלנו סורקת ברקע את מאגרי המשטרה וכ-20 עיריות, ושולחת התראה לוואטסאפ ולמייל ברגע שנרשם דוח על שמך — לפני שמכתב יוצא בכלל בדואר. בלי זה, רוב הנהגים מגלים את הדוח כשהוא כבר הוכפל וצברה ריבית פיגורים של 50%.

האם יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא להיות מכוסה לפני שזה קורה? 🛡️
```

*Variant B, problem-first (for A/B testing):*

```
היי {{name}}, רגע — לפני שאתה ממשיך את היום, שאלה קצרה.

קיבלת לאחרונה דוח שהפתיע אותך, או מכתב מהמשטרה שהגיע באיחור? כי זה בדיוק מה ש-Road Protect בונה כדי למנוע. אני סוכן AI דיגיטלי של השירות, ופוגש אותך כי השארת אצלנו פרטים בעבר.

אנחנו סורקים את מאגרי הרשויות 24/7 ומתריעים בוואטסאפ ובמייל ברגע שדוח נרשם — לפני שהוא הופך לכפל קנס.

האם זה רלוונטי עבורך עכשיו?
```

**Touch 2 — Light nudge** (+72h, only if no reply):

```
היי {{name}}, רק רציתי לוודא שההודעה הקודמת הגיעה.

חבל לפספס — נהג ממוצע בישראל מקבל 2 דוחות בשנה, וברוב המקרים גם לא יודע שהם נרשמו עד שמגיע מכתב עם כפל קנס בדואר.

האם יש משהו ספציפי שתרצה לבדוק, או שעדיף שאשלח לך פעם אחת קישור עם הפרטים?
```

**Touch 3 — Final value reframe, soft door-close** (+5 days; the reform is the real reason this lands now):

```
היי {{name}}, ההודעה האחרונה ממני בסבב הזה — אני לא רוצה להציק.

הסיבה שבחרנו לפנות אליך היא שבמהלך 2026 הרפורמה בתעבורה משנה את כל המסלול של ערעורים. דוחות הופכים להליך מנהלי, וטעות בניסוח הערעור עלולה לעלות באלפי שקלים ובנקודות. זה בדיוק הרגע להיות מוגן.

אם תרצה לבדוק מה רלוונטי עבורך — הקישור כאן: {{plan_link}}

ואם בכלל לא מעניין — אין בעיה. רק תכתוב לי "הסר", ואני מוודא שלא נחזור.
```

**Key branches.** *If they ask about a specific fine* → route to the appeals desk, don't collect details:

```
אל תשלם/י לפני שתבדוק/י! המומחים שלנו במחלקת הערעורים יבחנו את הדוח וימקסמו את סיכויי ביטול הקנס והנקודות עבורך תוך כמה דקות. כדי להתחיל, פשוט שלח/י 'היי' למחלקת הערעורים כאן: {{appeals_link}}
```

*If they push back ("not interested")* — one light deflection, then stop:

```
אין בעיה. רק כדי שזה לא יפתיע אותך בעתיד — נהג ממוצע מקבל 2 דוחות בשנה, ובמעל 60% מהמקרים המכתב מגיע אחרי תאריך התשלום. רוב הנהגים מגלים על דוח דרך הריבית, לא דרך הדוח עצמו. מוזמן לחזור אלינו אם הסיפור הזה ייגע אותך — ועד אז, נסיעה בטוחה. 🛡️
```

---

### C2 — Trademobile free-year user *with* fines

- **Who:** someone on the free Trademobile year who already has detected fines.
- **Goal:** upgrade them to VIP so we actually handle the fines.
- **Tone:** service-led ("we already caught these for you"), upgrade-framed, never apologetic. The opening message changes by **how many fines** they have.
- **Must, in message 1:** state that we're reaching out *because* of their Trademobile car purchase — that's why we have their details, and the free monitoring year came from that deal. Name Trademobile, never "leasing."

**Touch 1 — Service-led upgrade pitch.** *Variant for 1 fine:*

```
היי {{name}}, כאן Road Protect 🛡️

אנחנו פונים אליך כי עם רכישת הרכב שלך בטרייד מוביל קיבלת מאיתנו שנת ניטור והתראות על דוחות במתנה — ובתקופה הזו המערכת שלנו איתרה דוח אחד פתוח על שמך. החדשות הטובות — הוא תפוס בזמן, לפני שהוא צובר ריבית פיגורים של 50% או הופך לכפל קנס.

החדשות הפחות טובות — במסלול האיתור החינמי שלך, אנחנו רק מתריעים. הטיפול בדוח עצמו (ניסוח ערעור, התעסקות עם הרשות, מאבק על ביטול הנקודות) נשאר עליך.

במסלול VIP המומחים שלנו מטפלים בכל זה במקומך, וסופגים גם את ריבית הפיגורים אם בכלל תיווצר במהלך הטיפול. רוצה לשמוע איך זה נראה בפועל עבור הדוח הספציפי שלך?
```

*Variant for 2–3 fines:*

```
היי {{name}}, כאן Road Protect 🛡️

אנחנו פונים אליך כי עם רכישת הרכב בטרייד מוביל קיבלת מאיתנו שנת ניטור והתראות במתנה — ובתקופה הזו המערכת שלנו איתרה {{fines_count}} דוחות פתוחים על שמך. זה כבר לא מקרה בודד — זה דפוס שצריך טיפול ממוקד.

במסלול האיתור החינמי אנחנו מתריעים על הדוחות, אבל לא נכנסים פנימה. המומחים שלנו במסלול VIP מטפלים בכל הדוחות במקביל: מנסחים את הערעורים, נלחמים על ביטול הנקודות, וסופגים ריבית פיגורים אם נצברת תוך כדי.

זה בדיוק הסוג של מצב שבו השדרוג מחזיר את עצמו בקלות — דוח אחד שמתבטל מכסה את כל המינוי לכמה שנים. מעוניין לראות איך מטפלים בערימה הזאת ביחד?
```

*Variant for 4+ fines:*

```
היי {{name}}, כאן Road Protect 🛡️

אנחנו פונים אליך כי עם רכישת הרכב בטרייד מוביל קיבלת מאיתנו שנת ניטור והתראות במתנה. בתקופה הזו איתרנו {{fines_count}} דוחות פתוחים על שמך, וזה הרבה. ברמה הזאת של דוחות, כל יום שעובר זה ריבית פיגורים שמצטברת, נקודות שעולות, ופוטנציאל אמיתי להליכי גבייה.

במסלול VIP המומחים שלנו לוקחים את כל הערימה הזאת על עצמם — ערעורים על כולם, ניהול מול הרשויות, וטיפול בריבית הפיגורים. זה לא 'אולי נוכל' — זה ההתמחות שלנו.

חשוב לי להבין: יש דוח ספציפי שהכי דחוף לטפל בו עכשיו? נתחיל ממנו ונבנה את התמונה.
```

**Touch 2 — Cost-of-inaction reframe** (+5 days):

```
היי {{name}}, רק לוודא שלא פיספסת — הדוחות שאיתרנו עדיין פתוחים.

לפני שזה הופך לכפל קנס: ברגע שדוח עובר את תאריך התשלום, הוא קופץ אוטומטית ב-50%. אם הוא מצטרף לרביעי בתוך שלוש שנים — מוכפל שוב. זה לא תרחיש קצה, זה הברירת מחדל של המערכת.

במסלול VIP אנחנו עוצרים את כדור השלג עוד לפני שהוא מתחיל. מעוניין שאשלח לך את הקישור עם הפרטים? {{plan_link}}
```

**Touch 3 — Math close** (+7 days):

```
היי {{name}}, פעם אחרונה ממני בסבב הזה.

המתמטיקה פשוטה: ב-VIP העלות היא ₪35 לחודש (ובחיוב שנתי חוסכים עוד 20%). דוח אחד של מהירות שנחסך — ₪750. אחד שמשובש בנקודות — שווה הרבה יותר, כי קורסי נהיגה מונעת + ביטוח רכב שמתייקר. השדרוג משלם את עצמו על דוח אחד מבוטל.

הקישור כאן: {{plan_link}}

ואם זה לא הזמן — אין בעיה, אני סוגר את הסבב ולא אחזור. תכתוב לי "הסר" אם תרצה גם להסיר את עצמך מעדכוני המערכת.
```

**Key branches.** *"What's in VIP that I don't have now?"*

```
שלוש שכבות שאתה לא מקבל היום:

1. ערעורים בלתי מוגבלים — המומחים שלנו מנסחים, אתה חותם, אנחנו מטפלים מול הרשות.
2. ספיגת ריבית פיגורים — אם נצברת ריבית בזמן שהדוח אצלנו בטיפול, היא עלינו.
3. תשלומים מול העיריות + הפניה לעו"ד מומחה אם המקרה דורש את זה.

הפרטים המלאים כאן: {{plan_link}}
```

*Price objection ("יקר"):*

```
אני מבין. בוא נסתכל על זה ככה: דוח אחד של מהירות (₪750) שמתבטל — מכסה כמעט שנתיים של VIP. אם איתרנו לך {{fines_count}} דוחות פתוחים, הסיכוי שלפחות אחד נופל באחת הקטגוריות שניתן לערער עליהן — גבוה מאוד.

המסלול הוא לא הוצאה, הוא ביטוח שמשלם את עצמו ברגע שהוא מצליח. מעוניין שאסביר איזה דוחות בדרך כלל הכי קל לערער?
```

---

### C3 — Past-customer win-back

- **Who:** someone whose paid plan lapsed, and we've found new fines since.
- **Goal:** reactivate them on VIP. **No coupon** — we close on value, not a discount.
- **Tone:** warm acknowledgment of the history, no guilt, concrete proof we never stopped scanning. The opening changes by **how long ago they lapsed** (fresh / a few months / over a year).

**Touch 1 — Reactivation with proof.** *Fresh lapse (under ~2 months):*

```
היי {{name}}, כאן Road Protect 🛡️

הצטרפת אלינו בעבר, ואחרי שהמינוי נגמר — המערכת המשיכה לסרוק את המאגרים ברקע (זה חלק מהמודל שלנו). ומאז שעזבת, איתרנו עבורך {{fines_count}} דוחות פתוחים שעדיין דורשים טיפול.

לא רציתי שתלך לאיבוד עם זה. במסלול ה-VIP המומחים שלנו ייקחו את הדוחות האלה — ניסוח ערעור, מאבק על ביטול הקנס והנקודות, סופגים גם ריבית פיגורים שנצברה בינתיים.

רוצה לעבור על הדוחות הספציפיים שאיתרנו?
```

*A few months lapsed:*

```
היי {{name}}, כאן Road Protect 🛡️

עברו {{months_since_lapse}} חודשים מאז שסיימת איתנו, וברקע המערכת המשיכה לעבוד. איתרנו {{fines_count}} דוחות חדשים על שמך מאז שעזבת — כולם פתוחים, חלק מהם כבר התחילו לצבור ריבית פיגורים.

זה לא הזמן לבזבז עליהם כסף סתם. במסלול VIP המומחים שלנו לוקחים את הסיפור על עצמם — ערעור על כל דוח, ביטול נקודות, וטיפול מול הרשויות.

תרצה שאחזיר אותך פעיל ונתחיל מהדוח הכי דחוף?
```

*Over a year lapsed (discloses AI, like cold):*

```
היי {{name}}, כאן Road Protect 🛡️

עברה תקופה מאז שהיינו בקשר, אבל מערכת ההגנה שלנו ממשיכה לסרוק את המאגרים. אני סוכן AI דיגיטלי, ופונה כי איתרנו עבורך {{fines_count}} דוחות פתוחים שלא טופלו.

ייתכן שעד היום לא ראית את כל ההודעות הקודמות. הדוחות פעילים — חלקם כבר עם ריבית פיגורים. במסלול VIP אנחנו יכולים לקחת על עצמנו את הטיפול בכולם בבת אחת.

האם תרצה שאחזיר אותך פנימה ונראה איך מנקים את הסיפור הזה?
```

**Touch 2 — Cost-of-waiting reminder** (+4 days):

```
היי {{name}}, רק להוודא — הדוחות שאיתרנו עדיין פתוחים.

הם לא נעלמים בעצמם. כל יום שעובר מקרב אותם לתאריך כפל הקנס (₪750 שהופך ל-₪1,500), ולסבב גבייה רשמי. המומחים שלנו ב-VIP יודעים בדיוק על איזה סעיפים לערער ברשויות הספציפיות שמטפלות בדוחות שלך.

רוצה לראות איך זה נראה מהצד שלנו? {{plan_link}}
```

**Touch 3 — Last call** (+7 days, no coupon):

```
היי {{name}}, פעם אחרונה ממני.

הדוחות שאיתרנו על שמך עדיין פתוחים, והם רק מתקרבים לכפל קנס ולסבב גבייה. המומחים שלנו ב-VIP יכולים לקחת את כל הסיפור על עצמם — ערעור על כל דוח, מאבק על ביטול הקנס והנקודות, וספיגת ריבית פיגורים שנצברה בינתיים.

זה הזמן לעצור את הדוחות שמצטברים. {{plan_link}}

ואם זה לא הזמן, אין בעיה. תכתוב לי "הסר" אם תרצה גם להסיר את עצמך מההתראות שלנו.
```

**Key branches.** *"Why did you keep my data after I cancelled?"* (a fair question — handle with care):

```
שאלה טובה. כשמינוי נגמר, אנחנו ממשיכים לסרוק רק את הזיהויים שכבר היו לנו (מספר רכב + ת.ז.) כדי שאם דוח חדש מופיע, נוכל לתת לך את ההזדמנות לטפל בו לפני שהוא הופך לכפל קנס. שמירת המידע היא במסגרת תנאי השימוש שאישרת. אם תרצה שנמחק את הזיהויים שלך לחלוטין — אעביר אותך לנציג שיטפל בזה. רוצה?
```

*"I sold the car":*

```
תודה שעדכנת — חשוב לדעת. הדוחות שאיתרנו על שמך ייתכן והם מתקופה שהרכב היה אצלך, אז עדיין רלוונטיים אליך אישית. אבל אם כולם מתקופה אחרי המכירה, ייתכן והבעיה היא שהבעלות לא הועברה נכון. תרצה שנעבור על הפרטים?
```

---

### C4 — Trademobile welcome (new car buyer)

- **Who:** someone who just bought a car via Trademobile (= just got the free year).
- **Goal:** welcome them, make the free protection feel valuable, earn the right to message them again. **Zero hard sell** — first impression.
- **Tone:** warm, slightly celebratory. This is the one scenario where touch 2 fires on the calendar even if they never replied — it's a service moment, not a nudge.
- **Must, in message 1:** state that this came from their Trademobile car purchase (already done in the opener: *"עם הרכישה ב-Trademobile…"*). That's the reason we're reaching out and the basis for the free year.

**Touch 1 — Welcome** (+2h after purchase). *Default:*

```
היי {{name}}, כאן צוות Road Protect — ברכות על הרכב החדש! 🚗

עם הרכישה ב-Trademobile, חבילת ההגנה שלנו הופעלה אצלך אוטומטית, חינם לשנה שלמה. אין מה לעשות עכשיו — הכל כבר רץ ברקע.

מה אנחנו עושים בזמן הזה: סורקים 24/7 את מאגרי המשטרה וכ-20 עיריות. ברגע שנרשם דוח על שמך, נשלח התראה לוואטסאפ ולמייל — בדרך כלל לפני שהמכתב מהמשטרה מגיע אליך בכלל. זה ההבדל בין לערער בזמן לבין לשלם כפל קנס + ריבית של 50%.

יש שאלה? כתוב לי כאן. ואם הכל ברור — נסיעה בטוחה, אנחנו ברקע. 🛡️
```

**Touch 2 — Month-1 check-in** (+30 days, fires regardless of reply). *If we found nothing:*

```
היי {{name}}, חודש מאז שהצטרפת אלינו ב-Road Protect. ⏱

המערכת סרקה ברקע {{events_count}} פעמים את מאגרי המשטרה והעיריות עבור הרכב שלך ({{plate}}) — ובינתיים, הכל נקי. אין דוחות פתוחים על שמך.

ככה זה אמור להיות. אנחנו ממשיכים. אם משהו יוצץ — תקבל הודעה כאן מיד.

(ושאלה אחת אם מעניין: רוצה לראות איזה רשויות בדיוק אנחנו סורקים? אני זמין.)
```

*If we found a fine (soft VIP intro, not a hard upgrade push):*

```
היי {{name}}, חודש מאז שהצטרפת אלינו ב-Road Protect. ⏱

המערכת איתרה במהלך החודש {{events_count}} דוח/ות על שמך עבור הרכב {{plate}}. שלחנו לך התראה בזמן אמת — ככה זה אמור לעבוד.

הדוחות פתוחים. במסלול האיתור הנוכחי שלך, הטיפול עליך (ניסוח ערעור, הגשה לרשות, מאבק על הנקודות). במסלול VIP אנחנו לוקחים את כל זה על עצמנו.

תרצה לעבור על הדוח/ות שאיתרנו? נדבר כאן.
```

**Key branches.** *"Which authorities do you scan?"*

```
משטרת ישראל + מעל 20 עיריות, ביניהן תל אביב, ירושלים, חיפה, ראשון לציון, פתח תקווה, אשדוד, נתניה, באר שבע, חולון, בני ברק, רמת גן, אשקלון, רחובות, בת ים, הרצליה, כפר סבא, חדרה, מודיעין, נצרת, לוד, רעננה ועוד.
```

*Opt-out (warn them first — opting out kills future fine alerts):*

```
לפני שאני מוודא — אם תוסר מההתראות, גם הודעות על דוחות שיופיעו על שמך לא יישלחו. זה חבילת השירות החינמית שלך. עדיין להסיר?
```

---

### C5 — Free user just got a fine (real time)

- **Who:** a free/Detection user the moment our radar finds a new fine. **Highest-priority scenario** — pre-empts everything.
- **Goal:** empathy first, then convert to VIP (or the ₪49 one-off appeal as a softer option).
- **Tone:** empathetic first (*"איזה באסה"*), strategic second, sales last. The opening changes by **violation type** (speed / parking / phone / red light / other). Every touch 1 offers a **real choice**: the ₪49 one-off or VIP.

**Touch 1 — Empathy + dual choice.** *Speed camera:*

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
2️⃣ VIP — ₪35/חודש, ערעורים בלתי מוגבלים על כל דוח שיופיע + ספיגת ריבית פיגורים. עדיף אם זה לא הדוח הראשון או האחרון שלך.

איזה כיוון מתאים לך? אני סוכן AI דיגיטלי וכאן לעזור.
```

*Parking:*

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
2️⃣ VIP — ₪35/חודש, הכל פנימה.

איזה מתאים? אני כאן.
```

*Phone while driving:*

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
2️⃣ VIP — ₪35/חודש, הכל פנימה לכל דוח עתידי.

איזה מתאים לסיטואציה שלך?
```

*Red light:*

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
2️⃣ VIP — ₪35/חודש, הגנה מלאה.

מומלץ לטפל בזה מהר. איזה מתאים?
```

**Touch 2 — Cost-of-waiting** (+24h if no reply):

```
היי {{name}}, רק לוודא — הדוח שאיתרנו ({{fine.violation_type}}, ₪{{fine.amount}}) עדיין פתוח.

זה לא דחיינות שלי, זה זמן ספציפי: אחרי 90 יום מתאריך הדוח, הסכום קופץ ב-50% אוטומטית, וזה לא ניתן להחזרה. אם תרצה לערער — הזמן עכשיו, לא בעוד חודש.

הדרך הכי קצרה לטפל בזה היא או ערעור נקודתי ב-₪49, או לעבור ל-VIP ולסגור את הסיפור על כל דוח עתידי. תרצה שאעבור איתך על האפשרויות?
```

**Touch 3 — Final, gentle** (+5 days; if still no bite, hands off to C7's coupon track):

```
היי {{name}}, פעם אחרונה ממני בנושא הדוח שאיתרנו.

אני מבין שזה לא היה רגע נוח, ואני לא רוצה להציק. רק שתדע: עוד שבועיים-שלושה הדוח עובר לסטטוס של גבייה רשמית והאופציות לערער מצטמצמות בצורה משמעותית.

אם תרצה לדבר — אני כאן. אם לא — נסיעה בטוחה.

({{plan_link}} עדיין זמין.)
```

**Key branches.** *Frustration / venting* — empathy first, gender-mirrored. *Masculine:*

```
מבין אותך לגמרי, דוח כזה זה הדבר האחרון שצריך על הראש. זה הכי מבאס להרגיש ש'תפסו' אותך באמצע היום.

אבל אל תתייאש — הרבה דוחות מהסוג הזה מתבטלים בגלל פגמים בתיעוד או באכיפה. המומחים שלנו יודעים בדיוק איפה לחפש את הנקודות האלו ולערער. חבל לשלם ₪{{fine.amount}} ולצבור נקודות אם יש סיכוי לבטל.

רוצה שאשלח לך את הפרטים? נתחיל ב-₪49 ערעור נקודתי, או נעבור על VIP אם זה דפוס.
```

*Feminine:*

```
מבין אותך לגמרי, דוח כזה זה הדבר האחרון שצריך על הראש. זה הכי מבאס להרגיש ש'תפסו' אותך באמצע היום.

אבל אל תתייאשי — הרבה דוחות מהסוג הזה מתבטלים בגלל פגמים בתיעוד או באכיפה. המומחים שלנו יודעים בדיוק איפה לחפש את הנקודות האלו ולערער. חבל לשלם ₪{{fine.amount}} ולצבור נקודות אם יש סיכוי לבטל.

רוצה שאשלח לך את הפרטים? נתחיל ב-₪49 ערעור נקודתי, או נעבור על VIP אם זה דפוס.
```

*"I'll just pay it":*

```
אם תשלם עכשיו, אתה בעצם מודה בעבירה — והנקודות נרשמות אוטומטית ברישיון. הנקודות נצברות ויכולות להוביל לקורס נהיגה מונעת או פסילה. ערעור מעמיד את הדוח לבדיקה אמיתית — בהרבה מקרים מבטל את הקנס וגם את הנקודות.

₪49 לערעור נקודתי על הדוח הזה — שווה את הניסיון כשהאלטרנטיבה היא ₪{{fine.amount}} + נקודות. רוצה לנסות?
```

---

### C6 — Free year about to end

- **Who:** Detection / Trademobile-free users approaching expiry. Four touches: 30 days out, 14, 3, and day-of.
- **Goal:** convert to paid (VIP preferred, Detection acceptable) before protection switches off. **No coupon.**
- **Tone:** proof-of-value first ("here's what we did for you"), then what they'd lose, never desperation. Opening changes by whether we **found fines** during their year.

**Touch 1 — 30 days out, proof of value.** *Had fines:*

```
היי {{name}}, כאן Road Protect 🛡️

חודש מהיום, ההגנה שלך החינמית מסתיימת. רציתי לעצור רגע לפני זה ולהראות לך מה עשינו עבורך השנה.

המערכת סרקה {{scans_count}} פעמים את מאגרי המשטרה והעיריות עבור {{plate}}. במהלך הזה איתרנו {{fines_count}} דוחות על שמך — וזה בדיוק מה שמנע מהם להגיע אליך בדואר רק כשהם כבר הפכו לכפל קנס.

מצרף לך כאן גם את ייפוי הכוח שחתמת עליו כשהצטרפת — שיהיה לך מול העיניים שאתה כבר חלק מהשירות, והכל רשמי ומסודר.

בעוד 30 יום זה נעצר. השאלה הפשוטה: לעבור ל-VIP כדי להמשיך עם טיפול מלא (כולל הערעורים), או לכל הפחות להאריך את האיתור החינמי בתעריף השוטף?

הפרטים כאן: {{plan_link}}
```

*Attachment (build): touch 1 also carries the user's **signed power-of-attorney as a real WhatsApp document** (`{{poa_document}}`, pulled per user) — not just the text line. Seeing their own signed authorization is the trust trigger: "oh, I really did sign this, I'm already in the system." If no signed POA is on file for a user, drop both the attachment and the sentence that references it.*

*No fines:*

```
היי {{name}}, כאן Road Protect 🛡️

חודש מהיום, ההגנה החינמית שלך מסתיימת. רציתי לעצור רגע לפני זה.

השנה הזאת המערכת סרקה {{scans_count}} פעמים את מאגרי הרשויות עבור הרכב שלך ({{plate}}). התוצאה: אפס דוחות. ככה זה אמור להיות.

אבל — שנה ללא דוחות לא אומרת שגם השנה הבאה תהיה כזאת. רוב הנהגים שלנו מקבלים את הדוח הראשון שלהם דווקא בתקופות "השקטות." בעוד 30 יום, ההגנה הזאת מפסיקה אלא אם תמשיך.

VIP נותן לך גם את הטיפול בדוח אם וכשיופיע — לא רק התראה. הפרטים: {{plan_link}}

מה הכי הגיוני עבורך?
```

**Touch 2 — 14 days out, cost-of-lapse:**

```
היי {{name}}, שבועיים נשארו עד שההגנה שלך מסתיימת.

מה זה אומר בפועל: אחרי {{days_remaining}} ימים, המערכת מפסיקה לסרוק. אם יופיע דוח חדש על שמך — לא נדע, ולא תקבל התראה. הוא יגיע אליך רק כשהמכתב יגיע בדואר, מה שלרוב קורה אחרי שהוא כבר התחיל לצבור ריבית פיגורים.

זה לא משחק נפסיכולוגי, זה איך המערכת המנהלית בנויה.

VIP ב-₪35 לחודש (חיוב שנתי חוסך 20%), או איתור ב-₪99 לשנה אם אתה מעדיף להמשיך רק עם ההתראה. {{plan_link}}

איזה מתאים?
```

**Touch 3 — 3 days out, last call:**

```
היי {{name}}, שלושה ימים.

ביום [{{expires_at}}] ההגנה שלך מסתיימת אוטומטית, והרכב {{plate}} יוצא מתוך הסריקה שלנו. בלי שדרוג, לא נוכל יותר להתריע על דוחות חדשים.

אם זה לא הזמן הנכון — אין בעיה, אנחנו לא מחייבים אוטומטית. אם כן — {{plan_link}}.

ואם יש משהו ספציפי שמעכב — תכתוב לי, נראה איך לעזור.
```

**Touch 4 — Day-of** (only if we found ≥1 fine during the year):

```
היי {{name}}, היום ההגנה החינמית שלך מסתיימת — ולא רציתי לוותר בלי לנסות פעם אחרונה.

השנה איתרנו {{fines_count}} דוחות עבורך. זה לא היה תיאורטי. בלי המשך ההגנה, אם תופיע עוד עבירה — תגלה אותה בדואר, לרוב כשהיא כבר צברה ריבית פיגורים.

VIP ממשיך את הניטור *וגם* נותן לך טיפול מלא בערעור על כל דוח. {{plan_link}}

אם זה לא הזמן — תכתוב "הסר" ולא נחזור.
```

**Key branches.** *"Can I downgrade to Detection instead of VIP?"* — yes, way better than lapsing:

```
בהחלט. איתור הוא ₪99/שנה (₪8.25 לחודש), שומר על ההתראה ועל הסריקה 24/7. הטיפול בערעור עצמו עליך — אבל לפחות אתה יודע ולא מופתע. הקישור: {{plan_link}} (תוכל לבחור מסלול בדף).

אם תרצה לדעת מה אתה מפסיד אם לא תעבור ל-VIP — אני יכול להסביר.
```

*"Do you actually cancel fines?"* — no guarantees:

```
המומחים שלנו מכירים את הסעיפים והפרצות שבהם ניתן לערער. דוחות רבים מתבטלים בגלל פגמים בנוהל, באכיפה או בתיעוד. אנחנו לא מבטיחים ביטול של כל דוח — אבל אנחנו מבטיחים שניתן לדוח שלך את ההזדמנות הכי טובה האפשרית. רוצה לראות איך זה עובד? {{plan_link}}
```

---

### C7 — "Dirty & quick": abandoned appeal (the only coupon scenario)

- **Who:** someone who started a single appeal and didn't finish (or viewed a fine and didn't start checkout).
- **Goal:** get them to **finish that appeal** with 30% off. **Not** a VIP pitch — VIP comes later, separately.
- **Tone:** direct, slightly urgent, human. Highest over-sell risk — audit constantly. Touch 1 has **no coupon**; touch 2 introduces SAVE30; touch 3 is the same coupon as a deadline reminder (no bigger discount).

**Touch 1 — Nudge, no coupon** (+24h):

```
היי {{name}}, כאן צוות Road Protect 🛡️

ראיתי שהתחלת אצלנו תהליך ערעור על הדוח של {{fine.violation_type}} אבל לא סגרנו את זה. חבל להשאיר פתוח — דוח שלא מטופל בזמן צובר ריבית פיגורים של 50% וממשיך להסתבך.

רוצה שנסיים את הערעור? כל מה שנשאר זה להשלים את התהליך כאן: {{appeal_link}}

או שיש משהו ספציפי שעצר אותך?
```

**Touch 2 — 30% coupon on the appeal** (+3 days):

```
היי {{name}}, אני מבין שאולי המחיר הוא העיכוב.

סידרתי לך 30% הנחה על הערעור הנוכחי — הקוד: {{coupon_code}}. תקף 7 ימים.

המומחים שלנו ייקחו מכאן את הטיפול וילחמו למקסם את סיכויי ביטול הדוח והנקודות עבורך. כל מה שצריך זה להשלים את הערעור כאן: {{appeal_link}}

אם עדיין לא מתאים — אין בעיה. רק תכתוב לי "הסר" אם תרצה גם להסיר את עצמך מהתראות.
```

**Touch 3 — Last call, same coupon** (+5 days):

```
היי {{name}}, פעם אחרונה ממני בנושא הזה.

הקוד {{coupon_code}} (30% על הערעור) תקף עוד יומיים. אחרי זה הדוח פשוט ממשיך לצבור ריבית פיגורים, וחבל.

אם זה הזמן — מסיימים כאן בכמה דקות: {{appeal_link}}. ואם לא — לא אחזור על זה.
```

**Key branches.** *"How do I use the coupon?"*

```
פשוט: כנס/י ל-{{appeal_link}}, ובמעמד התשלום יש שדה להזין את הקוד {{coupon_code}}. המחיר יתעדכן אוטומטית עם 30% הנחה על הערעור. ברגע שתסיים/י, המומחים שלנו מקבלים את הדוח ומתחילים לטפל מיד.
```

*Price objection ("עדיין יקר"):*

```
אני מבין. אבל שווה לחשוב כמה עולה לך *לא* לטפל בדוח — הקנס עצמו + ריבית פיגורים של 50% + נקודות שיכולות לחייב קורס נהיגה מונעת. עם 30% ההנחה, הערעור יוצא זול בהרבה מהסיכון. רוצה שנעבור על זה ביחד?
```

---

## 6. The inbound scenario — full texts

### B1 — Someone messages us first

- **Who:** anyone — subscriber, prospect, lapsed, curious.
- **Goal:** classify what they need in 1–2 messages and route them. Don't pitch before understanding.
- **Tone:** helpful, friendly, neutral until intent is known.

**Opening** (when they first message in, and we can't already tell what they want):

```
היי! תודה שפנית ל-Road Protect 🛡️

קיבלת דוח שאתה רוצה לטפל בו, או שתרצה להבין מה אנחנו עושים? אני סוכן AI דיגיטלי ופה כדי לעזור. אם תכתוב לי בקצרה מה הסיפור, אדע להפנות אותך נכון.
```

Then the bot reads the message and routes to one of these:

**Got a fine** → straight to the appeals desk, no detail collection:

```
טוב שפנית לפני שביצעת תשלום! דוח שלא מטופל בזמן עלול לצבור ריבית פיגורים של 50% וכפל קנס, אז ממש שווה לבדוק לפני שמשלמים.

אל תשלם/י לפני שתבדוק/י — המומחים שלנו במחלקת הערעורים יבחנו את הדוח וימקסמו את סיכויי ביטול הקנס והנקודות עבורך. כדי להתחיל, פשוט שלח/י 'היי' למחלקת הערעורים כאן: {{appeals_link}}
```

**"What is this / are you lawyers?"** → short explainer + the legal line:

```
אנחנו שירות שעוזר לנהגים בישראל להתמודד עם דוחות תנועה. שלוש שכבות:

1. רדאר — סורקים 24/7 את מאגרי המשטרה וכ-20 עיריות אחר דוחות שנרשמים על שמך.
2. התראות — ברגע שמופיע דוח, נשלח התראה לוואטסאפ ולמייל — לרוב לפני שמכתב בכלל יוצא בדואר.
3. טיפול — המומחים שלנו במסלול VIP מנסחים את הערעור בשמך כדי לבטל את הדוח והנקודות.

לא משרד עורכי דין — כלי דיגיטלי שעוזר לך לנהל את הסיפור.

יש לך דוח עכשיו, או שזה לבירור כללי?
```

**"How much?"** → diagnostic first, then the right plan:

```
שלוש אופציות במחיר. כדי להתאים — שאלה אחת קודם: יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא הגנה כללית לעתיד?
```

The full plan summary, when they ask for all options:

```
שלושה מסלולים:
• איתור — ₪99/שנה (₪8.25/חודש). רדאר + התראות, הטיפול עליך.
• VIP — ₪35/חודש (חיוב שנתי חוסך 20%). הכל באיתור + ערעורים בלתי מוגבלים על ידי המומחים + ספיגת ריבית פיגורים + הפניה לעו"ד אם צריך.
• ערעור נקודתי — ₪49 חד פעמי. ערעור על דוח אחד, ללא הגבלת זמן לניצול.

איזה הכי מתאים לסיטואציה שלך?
```

**Complaint / "stop messaging me"** → acknowledge, flag internally, offer a human:

```
אני מצטער על התסכול. רוצה שאסביר מה קורה, או שתעדיף לדבר עם נציג?
```

**Wants a human** → hand off:

```
בכיף — אני מעביר אותך לנציג. הם יחזרו אליך בהקדם, ובינתיים אני כאן אם יש משהו אחר.
```

Other routes (handled the same way, sent to the right place): **account / cancel / billing** → email info@roadprotect.co.il or a human; **appeal status** (VIP) → handed to the team on the case; **company fleet** → "our CEO will be in touch"; **couldn't understand** → one clarifying question, then a human if still unclear.

---

## 7. The data that makes it personal

The bot is only as good as what it knows about the person. Our internal CRM holds **one row per driver**, and the bot reads it **live, right before every message**, so it always speaks from the latest truth.

### 7.1 What we know about each person

| What we know | Why it matters to the conversation |
|---|---|
| **Name** | personalize the greeting (never guess) |
| **Phone** | their WhatsApp identity |
| **Source / "root"** (Trademobile / private / ad / Pango) | picks the scenario *and* the wording |
| **Current plan** (Detection / VIP / free Trademobile / one-off / none / lapsed) | the single biggest routing lever |
| **Active fines (count)** | creates urgency; the real number goes in the message |
| **Last fine date** | lets us message right after a fresh fine |
| **Appeal stage** (none → started → submitted → rejected/approved) | whether to push, stay quiet, or be gentle |
| **Plan end date** | drives the "your year is ending" flow |
| **Days since we last talked** | how warm they are + frequency limits |
| **Sentiment** (bot fills this in from replies) | softens or stops pushy messages |
| **Churn risk & customer value** | how hard to push, when to back off |

The bot only **writes back** two things: the sentiment it read from a reply, and the "last talked" timestamp. Everything else it just reads.

### 7.2 How the data picks the scenario

The two biggest levers are **Source** and **Fines**:

- Trademobile + just bought a car → **C4 welcome**
- Trademobile + free year + has fines → **C2**
- Private / ad + never subscribed → **C1 cold**
- Anyone + a new fine just detected → **C5** (real-time)
- Anyone + started an appeal, didn't finish → **C7** (coupon)
- Lapsed + has fines → **C3 win-back**
- Anyone + plan ends within 30 days → **C6**

On top of that, the bot reads a simple **"warmth" level** (hot / warm / cold) that decides *how hard to push*. A hot user (paying, has fines, recently active, positive) gets a faster, more direct pitch; a cold or upset user gets a soft touch or nothing. If someone is upset **and** high churn-risk **and** silent for months, the bot goes quiet for 30 days — we don't make a bad situation worse.

### 7.3 How the data changes the *words*, not just the scenario

- **Source:** a Trademobile person hears *"השירות שקיבלת מטרייד מוביל"* and **never** "leasing." A private person hears the general pitch.
- **Fines count:** the *real* number. On a 3rd+ fine we can lean on the double-fine law for extra urgency.
- **Appeal stage:** if experts are already mid-appeal on a fine, the outbound bot says nothing about it — the human team owns it.
- **Gender:** mirrored from the first reply.
- **Honesty about detection:** we say "we detected your fine" only when our radar actually did. For someone who brought their own fine into an appeal, we say "the appeal you started."

A wrong detail — wrong gender, "leasing," a fine count that's off — breaks trust instantly. Accuracy is the product.

---

## 8. The rules that keep the bot from being annoying

- **Frequency caps** — at most 1 message per 24h, 3 per 7 days, 8 per 30 days, per person, across *all* scenarios. If two triggers fire back-to-back, the second waits its turn.
- **Quiet hours** — nothing 22:00–08:00, nothing during Shabbat (Fri evening → Sat evening), nothing on major holidays. A message that would land in a quiet window waits for the next open window. (Inbound is *always* answered.)
- **One scenario at a time** — if a person qualifies for two at once, the more urgent one wins (a fresh fine always beats a routine upsell) and the other waits.
- **Opt-out is sacred** — "remove me" (in its many Hebrew forms) stops everything immediately, everywhere, acknowledged in one message.
- **Escalate to a human** when it's beyond a bot: explicit request, legal threat, refund dispute, bereavement/illness, a complaint about the bot itself, or the bot misreading the same thing twice.

---

## 9. The dashboard

### 9.1 What it's for

So Yossi (and whoever runs growth later) can open one screen and answer the six questions that actually run the bot:

1. How many we reached, by scenario, last 7 days.
2. Reply rate for message 1 / 2 / 3, per scenario. *(Message-2 is the one Yossi specifically asked for — does the nudge work?)*
3. Conversion rate per scenario, and **which message closed it**.
4. Who flagged bad feedback or asked to cancel — **with names**.
5. Which cohort converts best (Trademobile vs cold vs lapsed).
6. Top objections in the last 30 days.

### 9.2 Plain definitions

- **Reached** = the message was delivered.
- **Engaged** = they replied at least once.
- **Converted** = they actually paid.
- **Conversion rate** = conversions ÷ reached.

### 9.3 The four screens

**Screen 1 — Overview (סקירה כללית).** The daily snapshot, Hebrew RTL, navy brand. Top row of KPI cards: total reached, total converted + ₪ revenue, opt-out rate (red if >2%), bad-feedback rate (red if >1%). Below them a **"what needs my attention"** strip that surfaces any scenario breaching a guardrail or any reply rate dropping. Then all 7 outbound scenarios as horizontal funnel bars (reached → reply 1 → reply 2 → reply 3 → converted → revenue), plus an inbound-bot summary panel (sessions, what people wanted, conversion, escalations).

**Screen 2 — Scenario funnel (פירוט תרחיש).** Pick one scenario, see the full drop-off: eligible → reached → replied at each touch → converted, with the drop between each step colored green/yellow/red. Plus: which message closed the conversions, A/B variant comparison, top objections, a scroll of recent real replies, the conversions list with revenue, and a guardrail strip (opt-out, bad-feedback, delivery failures, coupon redemption).

**Screen 3 — Conversations & quality / Users (משתמשים).** The "who" view — every number is **clickable down to the actual people**. Filter by event (replied / converted / opted-out / bad-feedback / escalated / mid-sequence), scenario, touch, plan, time. Each row: name, phone, scenario, **the exact text they sent**, date. Click a row for that person's full history and transcript. Exportable to CSV with a privacy note.

**Screen 4 — Cohorts (קוהורטות).** Up to three audiences side by side (default: Trademobile-warm vs cold vs lapsed) on the same funnel, best cohort in green, worst in light red. Plus each cohort's totals (reached, converted, rate, revenue, opt-out, bad-feedback, ARPU) and a chart of where new people enter the bot over time.

*(A small Settings screen covers time zone, default window, optional email digest, and guardrail thresholds.)*

### 9.4 The coupon view (C7 only)

How many **SAVE30** codes were **issued vs redeemed**, and the **share of appeal conversions that needed the coupon**. That last one is a guardrail: keep it under ~25%, or we're training people to wait for a discount.

### 9.5 How the UI feels

Hebrew RTL throughout (English is a later pass). Navy brand, white background, teal accents — it should feel like the live product. Desktop-first. Fast: home paints in under ~1.5s, switching the time window is near-instant. Charts have a "show data table" toggle, and guardrails use icons (✓ / ⚠️) as well as color. Visual reference: `mockups/dashboard.html`.

---

## 10. What we deliberately are NOT doing this round

- **No English** — the bot ships in Hebrew; translation is a separate later pass.
- **No new scenarios** — documenting and sharpening the existing 8, not inventing C8/B2.
- **No B2B partner messaging** (Pango, Strauss, etc.) — partner-side, a separate project.
- **No email / SMS** — WhatsApp only this round.
- **No dashboard logins/permissions, no real-time alerts** — internal team only for now; a clear daily view first.

---

## 11. The honest open gaps

- A **live "new fine just arrived" trigger** so C5 can fire the moment a fine lands.
- A **clear plan-tier flag** — today "paying" doesn't distinguish Detection from VIP.
- A **real opt-out flag** so "remove me" is a clean, reliable signal.
- An **auto-renew flag** so the "your year is ending" flow doesn't nag people who'll renew automatically.

---

## 12. How we'll know it worked

- **The spec is good** if the bot can be built straight from it — every scenario has its trigger, its messages, its timing, and its exit, with **no open "what do we do here?" gaps**.
- **The dashboard is good** if, within 30 days of launch, Yossi can answer all six questions in §9.1 unaided.
- **The bot is good** if reply rates and conversions per scenario are visible and improving, while opt-outs stay ≤2% and bad-feedback ≤1% per scenario per month.

---

*Plain-language companion to the build-ready spec. Source files: `bot-spec/` (per-scenario detail + cross-cutting rules), `dashboard-spec/` (metrics, events, funnel, screens), `mockups/dashboard.html` (visual reference). Those win on technical detail; this doc wins on "what & why & what it says."*
