# C2 — Trademobile Active Cohort with Detected Fines (v2)

**Scenario code**: `C2`
**Channel**: WhatsApp, C2B outbound
**Audience**: Users currently on the Trademobile free-Detection year, system has detected ≥1 fine for them
**Goal**: Convert from free Detection to paid VIP, using the detected fine(s) as the demonstration of value
**Tone**: Service-led ("we already caught these for you"), upgrade-framed, never apologetic

---

## Critique of current version (`06_bot/scenarios/c2b/02_trademobile_active.md`)

What's weak in the original:

1. **Identical body to C3.** The original explicitly notes "Same outbound template as C3 — this is probably leaving money on the table." It is. C2's audience is *currently protected*; C3's is *lapsed*. The framing must differ; sharing copy is lazy.
2. **No fine-count segmentation.** A user with 1 fine and a user with 5 fines hear the same message. They shouldn't — the 5-fines user is in active pain and should hear urgency; the 1-fine user is in observation mode and should hear leverage.
3. **No second touch.** Same single-touch problem as C1. For active free-tier users with detected fines, the cost of letting the conversation die after one message is high — these are the warmest non-paying users in the funnel.
4. **No timing relative to fine detection.** Should the message fire 1 hour after detection? 24 hours? 7 days into accumulation? Currently undefined; defaults to "when the trigger fires," which is whenever the orchestrator gets to it.
5. **B1/B2/B3 branches reference C2's "three concrete differentiators"** but don't specify when to send them — vendor will guess.
6. **The "free year" framing isn't surfaced enough.** The user got Trademobile-free; the next layer (VIP) is the natural upgrade story. Original message buries this.

What's strong (kept):

- The "המערכות שלנו איתרה עבורך X דוחות" hook is correct and proof-of-value.
- The math reframing in B3 (₪750 fine cancelled covers 1.5 years of VIP) is good.
- "המומחים שלנו" framing aligns with legal line.

---

## Trigger predicate

```
TRIGGER (C2):
  user.subscription = 'trademobile_free'
  AND user.subscription.started_at <= NOW() - INTERVAL '14 days'   -- past welcome window
  AND user.subscription.expires_at > NOW() + INTERVAL '60 days'    -- not in pre-expiry window (C6 owns that)
  AND (
    SELECT COUNT(*) FROM fines
    WHERE fines.user_id = user.id
    AND fines.detected_at >= user.subscription.started_at
    AND fines.status IN ('new', 'open', 'pending_appeal')
  ) >= 1
  AND user.opted_out = FALSE
  AND NOT EXISTS (C5 in 'entered' or 'replied' state)              -- C5 takes priority on fresh-fine moment
```

**Segmentation flag** (drives variant selection):

```
fine_count_bucket =
  CASE
    WHEN open_fines = 1 THEN 'single'
    WHEN open_fines BETWEEN 2 AND 3 THEN 'multiple'
    WHEN open_fines >= 4 THEN 'high'
  END
```

---

## Variables used

- `{{name}}` — `user.first_name`
- `{{fines_count}}` — count of open fines
- `{{plan_link}}` — UTM-tagged with `campaign=C2`

---

## Sequence

### Touch 1 — Service-led upgrade pitch (variant by fine count)

**Delay**: fires immediately when trigger satisfied (orchestrator next cycle)
**Variants**: A_single (1 fine), A_multiple (2–3), A_high (4+)
**Exit conditions**: `replied` → branches | `opted_out`
**Events emitted**: `touch.sent`, `touch.delivered`, `touch.replied`

#### Variant A_single — "we found one, let's not let it grow"

```
היי {{name}}, כאן Road Protect 🛡️

המערכת שלנו איתרה דוח אחד פתוח על שמך מאז שהצטרפת. החדשות הטובות — הוא תפוס בזמן, לפני שהוא צובר ריבית פיגורים של 50% או הופך לכפל קנס.

החדשות הפחות טובות — במסלול האיתור החינמי שלך, אנחנו רק מתריעים. הטיפול בדוח עצמו (ניסוח ערעור, התעסקות עם הרשות, מאבק על ביטול הנקודות) נשאר עליך.

במסלול VIP המומחים שלנו מטפלים בכל זה במקומך, וסופגים גם את ריבית הפיגורים אם בכלל תיווצר במהלך הטיפול. רוצה לשמוע איך זה נראה בפועל עבור הדוח הספציפי שלך?
```

#### Variant A_multiple — "you've got a stack — let's clear it"

```
היי {{name}}, כאן Road Protect 🛡️

המערכת שלנו איתרה {{fines_count}} דוחות פתוחים על שמך מאז שהצטרפת. זה כבר לא מקרה בודד — זה דפוס שצריך טיפול ממוקד.

במסלול האיתור החינמי אנחנו מתריעים על הדוחות, אבל לא נכנסים פנימה. המומחים שלנו במסלול VIP מטפלים בכל הדוחות במקביל: מנסחים את הערעורים, נלחמים על ביטול הנקודות, וסופגים ריבית פיגורים אם נצברת תוך כדי.

זה בדיוק הסוג של מצב שבו השדרוג מחזיר את עצמו בקלות — דוח אחד שמתבטל מכסה את כל המינוי לכמה שנים. מעוניין לראות איך מטפלים בערימה הזאת ביחד?
```

#### Variant A_high — "this is daily pain — we close it"

```
היי {{name}}, כאן Road Protect 🛡️

איתרנו {{fines_count}} דוחות פתוחים על שמך, וזה הרבה. ברמה הזאת של דוחות, כל יום שעובר זה ריבית פיגורים שמצטברת, נקודות שעולות, ופוטנציאל אמיתי להליכי גבייה.

במסלול VIP המומחים שלנו לוקחים את כל הערימה הזאת על עצמם — ערעורים על כולם, ניהול מול הרשויות, וטיפול בריבית הפיגורים. זה לא 'אולי נוכל' — זה ההתמחות שלנו.

חשוב לי להבין: יש דוח ספציפי שהכי דחוף לטפל בו עכשיו? נתחיל ממנו ונבנה את התמונה.
```

**Quality checklist (touch 1):**
- [x] Differentiated copy per fine-count bucket
- [x] Acknowledges current plan ("המסלול החינמי שלך") — respects the existing relationship
- [x] States the gap (alert vs. handling) clearly
- [x] Ends with question, not link-dump
- [x] Legal-line clean
- [x] 4 short paragraphs, gender-neutral

---

### Touch 2 — Cost-of-inaction reframe

**Delay**: +5 days after touch 1
**Variants**: A (single, all fine-count buckets receive this)
**Skip conditions**: replied, converted, opted out, suppressed, escalated
**Exit conditions**: same set
**Events emitted**: `touch.sent`, `touch.delivered`, optionally `touch.replied`

```
היי {{name}}, רק לוודא שלא פיספסת — הדוחות שאיתרנו עדיין פתוחים.

לפני שזה הופך לכפל קנס: ברגע שדוח עובר את תאריך התשלום, הוא קופץ אוטומטית ב-50%. אם הוא מצטרף לרביעי בתוך שלוש שנים — מוכפל שוב. זה לא תרחיש קצה, זה הברירת מחדל של המערכת.

במסלול VIP אנחנו עוצרים את כדור השלג עוד לפני שהוא מתחיל. מעוניין שאשלח לך את הקישור עם הפרטים? {{plan_link}}
```

---

### Touch 3 — Math close

**Delay**: +7 days after touch 2 (~14 days from touch 1)
**Variants**: A (single)
**Skip conditions**: same set
**Exit conditions**: after sending → `exhausted` (no new C2 for 90 days; if new fine detected, re-evaluates trigger)
**Events emitted**: `touch.sent`, `touch.delivered`, optionally `touch.replied`, eventually `sequence.exhausted`

```
היי {{name}}, פעם אחרונה ממני בסבב הזה.

המתמטיקה פשוטה: ב-VIP העלות היא ₪489 לשנה. דוח אחד של מהירות שנחסך — ₪750. אחד שמשובש בנקודות — שווה הרבה יותר, כי קורסי נהיגה מונעת + ביטוח רכב שמתייקר. השדרוג משלם את עצמו על דוח אחד מבוטל.

הקישור כאן: {{plan_link}}

ואם זה לא הזמן — אין בעיה, אני סוגר את הסבב ולא אחזור. תכתוב לי "הסר" אם תרצה גם להסיר את עצמך מעדכוני המערכת.
```

---

## Branches (when user replies)

### B1 — "What's in VIP that I don't have now?"
**Bot reply:**
```
שלוש שכבות שאתה לא מקבל היום:

1. ערעורים בלתי מוגבלים — המומחים שלנו מנסחים, אתה חותם, אנחנו מטפלים מול הרשות.
2. ספיגת ריבית פיגורים — אם נצברת ריבית בזמן שהדוח אצלנו בטיפול, היא עלינו.
3. תשלומים מול העיריות + הפניה לעו"ד מומחה אם המקרה דורש את זה.

הפרטים המלאים כאן: {{plan_link}}
```
**Event**: `branch.taken: vip_features`

### B2 — "I'll just pay the fines"
**Bot reply:**
```
אם תשלם עכשיו אתה בעצם מודה בעבירה — וסופג גם את הנקודות. הנקודות נרשמות ברישיון, מצטברות, ויכולות להוביל לקורס נהיגה מונעת או פסילה אם תהיה עוד אחת בעבירות. ערעור מעמיד את הדוח לבדיקה אמיתית, ובהרבה מקרים מבטל גם את הקנס וגם את הנקודות.

חבל לוותר על השכבה השנייה הזאת — רוצה שאסביר איך זה עובד בפועל?
```
**Event**: `branch.taken: pay_anyway`

### B3 — Price objection ("יקר")
**Bot reply:**
```
אני מבין. בוא נסתכל על זה ככה: דוח אחד של מהירות (₪750) שמתבטל — מכסה כמעט שנתיים של VIP. אם איתרנו לך {{fines_count}} דוחות פתוחים, הסיכוי שלפחות אחד נופל באחת הקטגוריות שניתן לערער עליהן — גבוה מאוד.

המסלול הוא לא הוצאה, הוא ביטוח שמשלם את עצמו ברגע שהוא מצליח. מעוניין שאסביר איזה דוחות בדרך כלל הכי קל לערער?
```
**Event**: `branch.taken: price_objection`, `objection.raised: price`

### B4 — "Already on free Detection, why upgrade?"
**Bot reply:**
```
שאלה טובה. ההבדל: היום אתה רואה את הדוח, אבל הטיפול ביד שלך — לכתוב את הערעור, להגיש בזמן, להתעסק עם הרשות. ב-VIP זה עובר אלינו, מקצה לקצה. במצב הנוכחי, אם איתרנו דוח ולא טיפלת בו — הוא ממשיך לצבור. במצב VIP — מתחילים לטפל ברגע שמאתרים.

מעוניין שנעבור על הדוחות הפתוחים שלך ביחד?
```
**Event**: `branch.taken: why_upgrade`

### B5 — User asks "who are you" / "are you a bot"
Per `00_overview.md` § 0.10 — disclose.

### B6 — Opt-out
Per § 0.8.

### B7 — Reply doesn't match any branch
Fall through to B1 inbound classifier.

---

## Suppression and exit

- **C5 fires (new fine detected)**: C2 pauses immediately. C5 takes over. If C5 closes without conversion, C2 *does not* resume — we don't want to immediately re-pitch after the user just declined VIP on a hotter trigger. C2 re-eligible only after 30 days.
- **C6 starts (pre-expiry)**: C2 ends with `expired`. C6 takes over.
- **Converted**: sequence ends, `converted` with plan + revenue captured.
- **Exhausted after touch 3**: no new C2 for this user for 90 days *unless* a new fine is detected (re-evaluates trigger and may re-enter).

---

## Events emitted

Same canonical event list as C1 (see C1 § "Events emitted in this scenario"). All carry `scenario = 'C2'`, `variant ∈ {A_single, A_multiple, A_high}`, `fine_count_bucket`, `touch_n`.

Additional events specific to C2:
- `bucket.assigned` — fired when fine_count_bucket is computed; allows the dashboard to track which buckets generate which conversion rates

---

## A/B testing slots

- **Touch 1 variant matrix** is already 3-way (single / multiple / high) but we can also A/B the *opening line* within each variant (warm vs. crisp).
- **Touch 2 cost-of-inaction** — test with vs. without the explicit "50% interest" math.
- **Touch 3 math close** — test "math" framing vs. "loss aversion" framing (next iteration).

---

## Open questions for Yossi

1. **Fine-count bucket boundaries**: are 1 / 2-3 / 4+ the right cuts? Could be 1 / 2-4 / 5+. Need to look at the actual distribution.
2. **What counts as a "detected fine" for trigger purposes**: any fine in the system, or only ones we've actually surfaced to the user via an alert? The user-experience of "we already alerted you about this" matters for the framing.
3. **C2 vs C7 overlap**: a Trademobile-active user who viewed a fine and didn't convert — does C7 fire? My read: C7 wins (it's higher priority, has the coupon lever), but worth confirming.
4. **"VIP" naming**: the bot is supposed to say "מסלול ה-VIP" or just "VIP"? Some current scenarios mix both. Standardize.
