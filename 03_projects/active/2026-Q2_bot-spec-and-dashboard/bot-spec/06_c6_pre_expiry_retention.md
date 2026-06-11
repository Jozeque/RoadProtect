# C6 — Pre-Expiry Retention (v2)

**Scenario code**: `C6`
**Channel**: WhatsApp, C2B outbound
**Audience**: Detection or Trademobile-free-year users whose subscription expires within 30 days
**Goal**: Convert from free → paid (VIP preferred, Detection acceptable) before protection lapses
**Tone**: "Here's what we did for you / here's what you'd lose" — proof-of-value first, FOMO second, never desperation

---

## Critique of current version (`06_bot/scenarios/c2b/06_pre_expiry_retention.md`)

What's weak in the original:

1. **Touch cadence mentioned as 30 / 14 / 3 / 0 days but only the 30-day message is written.** Three of the four planned touches are missing. Vendor would have to guess them.
2. **`{{events_count}}` defined loosely** as "fines detected / scans run." Pick one — they tell very different stories. ("We scanned 142k records for you" vs. "We detected 2 fines for you" are different conversations.)
3. **Missing later touches.** A user days from expiry who hasn't converted needs a last-call touch. (Note: **not** a coupon — per Yossi the 30% coupon is reserved for single-appeal abandoners (C7), not for discounting VIP at expiry. The closer here is the cost-of-lapse + a graceful door-close.)
4. **"לנהוג בלי Road Protect זה כמו לנהוג בלי ביטוח"** is a strong line but on a *welcome moment* equivalent (pre-expiry isn't a welcome). It's also a slight legal-line risk — comparing to insurance suggests guaranteed indemnification, which we don't provide.
5. **B2 ("I didn't get any fines this year, why pay?") reuses the same answer as objection_library.md** — fine, but doesn't customize for "you have a free year ending right now" context.
6. **No path for "I want to downgrade to Detection, not VIP."** Should be acknowledged — Detection (₪99) is way better than letting them lapse to nothing.

What's strong (kept):

- The "here's what we did" proof framing is correct
- The B1 explanation of Detection vs VIP is good
- The pricing math (one cancelled fine pays multiple years of VIP) is a strong closer

---

## Trigger predicate

```
TRIGGER (C6):
  user.subscription IN ('detection', 'trademobile_free')
  AND user.subscription.expires_at BETWEEN NOW() AND NOW() + INTERVAL '30 days'
  AND user.subscription.auto_renew = FALSE                  -- if they're already auto-renewing, no need to remind
  AND user.opted_out = FALSE
  AND NOT EXISTS (C5 in entered/replied state)              -- a fresh-fine event takes priority
```

**Touch scheduling derives from `expires_at`**:

| Touch | Fire when |
|---|---|
| 1 | `expires_at` − 30 days |
| 2 | `expires_at` − 14 days |
| 3 | `expires_at` − 3 days |
| 4 (optional, only if `fines_count >= 1`) | `expires_at` − 0 days (day-of last call, no coupon) |

If any touch lands inside quiet hours, defer to next open per § 0.7.

---

## Variables used

- `{{name}}`, `{{plate}}`, `{{plan_link}}`
- `{{scans_count}}` — total scans run for this user during their year (large number, "we worked hard")
- `{{fines_count}}` — fines detected during their year
- `{{days_remaining}}` — derived integer, used in touch 2/3/4 copy

**Decision**: spec uses `{{scans_count}}` AND `{{fines_count}}` as two separate variables. The original ambiguity (`{{events_count}}`) is resolved.

> **No coupon in C6.** VIP isn't discounted at expiry (Yossi: the price is already low, and the 30% coupon is reserved for single-appeal abandoners in C7). The last-call lever is the cost-of-lapse, not a price cut.

---

## Sequence

### Touch 1 — 30 days out: proof of value

**Delay**: `expires_at` − 30 days (calendar)
**Variants**: A_had_fines (≥1 fine detected during year), A_no_fines (zero fines detected — different framing)
**Skip conditions**: opted out | C5 already fired in last 14 days (let that conversation settle)
**Exit conditions**: standard
**Events emitted**: standard

#### Variant A_had_fines

```
היי {{name}}, כאן Road Protect 🛡️

חודש מהיום, ההגנה שלך החינמית מסתיימת. רציתי לעצור רגע לפני זה ולהראות לך מה עשינו עבורך השנה.

המערכת סרקה {{scans_count}} פעמים את מאגרי המשטרה והעיריות עבור {{plate}}. במהלך הזה איתרנו {{fines_count}} דוחות על שמך — וזה בדיוק מה שמנע מהם להגיע אליך בדואר רק כשהם כבר הפכו לכפל קנס.

בעוד 30 יום זה נעצר. השאלה הפשוטה: לעבור ל-VIP כדי להמשיך עם טיפול מלא (כולל הערעורים), או לכל הפחות להאריך את האיתור החינמי בתעריף השוטף?

הפרטים כאן: {{plan_link}}
```

#### Variant A_no_fines

```
היי {{name}}, כאן Road Protect 🛡️

חודש מהיום, ההגנה החינמית שלך מסתיימת. רציתי לעצור רגע לפני זה.

השנה הזאת המערכת סרקה {{scans_count}} פעמים את מאגרי הרשויות עבור הרכב שלך ({{plate}}). התוצאה: אפס דוחות. ככה זה אמור להיות.

אבל — שנה ללא דוחות לא אומרת שגם השנה הבאה תהיה כזאת. רוב הנהגים שלנו מקבלים את הדוח הראשון שלהם דווקא בתקופות "השקטות." בעוד 30 יום, ההגנה הזאת מפסיקה אלא אם תמשיך.

VIP נותן לך גם את הטיפול בדוח אם וכשיופיע — לא רק התראה. הפרטים: {{plan_link}}

מה הכי הגיוני עבורך?
```

---

### Touch 2 — 14 days out: cost-of-lapse

**Delay**: `expires_at` − 14 days
**Variants**: A (single — applies to both buckets, but copy references both)
**Skip conditions**: standard + converted in last 30 days
**Events emitted**: standard

```
היי {{name}}, שבועיים נשארו עד שההגנה שלך מסתיימת.

מה זה אומר בפועל: אחרי {{days_remaining}} ימים, המערכת מפסיקה לסרוק. אם יופיע דוח חדש על שמך — לא נדע, ולא תקבל התראה. הוא יגיע אליך רק כשהמכתב יגיע בדואר, מה שלרוב קורה אחרי שהוא כבר התחיל לצבור ריבית פיגורים.

זה לא משחק נפסיכולוגי, זה איך המערכת המנהלית בנויה.

VIP ב-₪489 לשנה (פחות מ-₪41 לחודש), או איתור ב-₪99 לשנה אם אתה מעדיף להמשיך רק עם ההתראה. {{plan_link}}

איזה מתאים?
```

---

### Touch 3 — 3 days out: last call before lapse

**Delay**: `expires_at` − 3 days
**Variants**: A (single)
**Skip conditions**: standard
**Events emitted**: standard

```
היי {{name}}, שלושה ימים.

ביום [{{expires_at}}] ההגנה שלך מסתיימת אוטומטית, והרכב {{plate}} יוצא מתוך הסריקה שלנו. בלי שדרוג, לא נוכל יותר להתריע על דוחות חדשים.

אם זה לא הזמן הנכון — אין בעיה, אנחנו לא מחייבים אוטומטית. אם כן — {{plan_link}}.

ואם יש משהו ספציפי שמעכב — תכתוב לי, נראה איך לעזור.
```

---

### Touch 4 — Day-of, last call (conditional, no coupon)

**Delay**: `expires_at` − 0 (fires on the actual expiry day, in the morning)
**Fires only if**: `fines_count >= 1` (we have leverage — they saw value in real time) AND no prior touch converted
**Variants**: A (single)
**Exit conditions**: after this touch → `exhausted`; user transitions to lapsed state, becomes eligible for C3 after the cooldown
**Events emitted**: standard

```
היי {{name}}, היום ההגנה החינמית שלך מסתיימת — ולא רציתי לוותר בלי לנסות פעם אחרונה.

השנה איתרנו {{fines_count}} דוחות עבורך. זה לא היה תיאורטי. בלי המשך ההגנה, אם תופיע עוד עבירה — תגלה אותה בדואר, לרוב כשהיא כבר צברה ריבית פיגורים.

VIP ממשיך את הניטור *וגם* נותן לך טיפול מלא בערעור על כל דוח. {{plan_link}}

אם זה לא הזמן — תכתוב "הסר" ולא נחזור.
```

**Why touch 4 is conditional**: a user with zero fines during the year has no concrete leverage point for a last call. For them, the sequence exhausts after touch 3. (Touch 4 is a deadline reminder for users who saw real value — not a discount.)

---

## Branches (when user replies)

### B1 — "What's the difference between what I have now and VIP?"
Per FAQ. The cleaner version from original is kept:
```
שאלה מצוינת. עד עכשיו היית במסלול האיתור — סרקנו, התרענו, אבל הטיפול בדוח עצמו עליך. ב-VIP המומחים שלנו לוקחים את הערעור על עצמם, נלחמים על ביטול הקנס והנקודות, וסופגים גם ריבית פיגורים אם היא מצטברת תוך כדי. זה המעבר מ'לדעת שיש בעיה' ל'לפתור את הבעיה.'

{{plan_link}}
```
**Event**: `branch.taken: tier_compare`

### B2 — "Why pay if I had no fines this year?"
**Bot reply** (adapted from objection_library, contextualized):
```
הלוואי וגם השנה הבאה תעבור נקייה — אבל זה לא בידינו. הכבישים מלאים במצלמות חדשות ובאכיפה מוגברת ב-2026. רגע אחד של חוסר תשומת לב, ופתאום קנס של אלפי שקלים + נקודות.

ה-VIP הוא רשת הביטחון. דוח אחד שמתבטל מחזיר את עלות המינוי לכמה שנים קדימה. אבל אם 'תמיד נקי' זה הסיפור — איתור ב-₪99 שומר לפחות על ההתראה. עדיף את זה מאפס. רוצה את הפרטים?
```
**Event**: `branch.taken: no_fines_objection`, `objection.raised: not_needed`

### B3 — "Can I downgrade to Detection instead of VIP?"
**Bot reply:**
```
בהחלט. איתור הוא ₪99/שנה (₪8.25 לחודש), שומר על ההתראה ועל הסריקה 24/7. הטיפול בערעור עצמו עליך — אבל לפחות אתה יודע ולא מופתע. הקישור: {{plan_link}} (תוכל לבחור מסלול בדף).

אם תרצה לדעת מה אתה מפסיד אם לא תעבור ל-VIP — אני יכול להסביר.
```
**Event**: `branch.taken: downgrade_request`

### B4 — "Do you actually cancel fines?"
Per FAQ — no guarantees:
```
המומחים שלנו מכירים את הסעיפים והפרצות שבהם ניתן לערער. דוחות רבים מתבטלים בגלל פגמים בנוהל, באכיפה או בתיעוד. אנחנו לא מבטיחים ביטול של כל דוח — אבל אנחנו מבטיחים שניתן לדוח שלך את ההזדמנות הכי טובה האפשרית. רוצה לראות איך זה עובד? {{plan_link}}
```
**Event**: `branch.taken: actually_cancels`

### B5 — Price objection
Per objection_library + context.

### B6 — "Just leave it / don't renew"
**Bot reply** (graceful):
```
מובן. בעוד {{days_remaining}} ימים ההגנה נכבית אוטומטית, אנחנו לא נחייב אותך. אם תרצה לחזור בעתיד — תמיד אפשר. נסיעה בטוחה. 🛡️
```
Mark scenario as `expired` (graceful non-conversion, not exhausted).
**Event**: `branch.taken: explicit_decline`, then `expired`

### B7 — Opt-out / B8 — Identity / B9 — Other
Standard.

---

## Suppression and exit

- **C5 mid-sequence**: pauses C6. C5 takes over. C6 resumes timing post-C5 if expires_at is still future.
- **Conversion at any touch**: `converted` with plan + revenue.
- **Auto-renew flipped on by user before touch 4**: sequence ends (achieved goal).
- **Exhausted (no convert through touch 3 or touch 4)**: user transitions to lapsed at expires_at. Becomes eligible for C3 after the 30-day cooldown if fines are detected post-lapse.

---

## Events emitted

Standard + C6-specific:
- `expiry.30d.sent`, `expiry.14d.sent`, `expiry.3d.sent`, `expiry.day_of.sent` — explicit named events for the dashboard's renewal-funnel view
- `auto_renew.enabled` — fires when user converts AND opts into auto-renew (separately trackable)

*(No `coupon.*` events — C6 doesn't issue coupons.)*

---

## A/B testing slots

- **Touch 1: had_fines variant — proof framing vs FOMO framing** (current is proof-first; FOMO-first is testable)
- **Touch 4 fires for no_fines users too** — current spec says no, but worth testing the inverse on a small slice (no coupon either way)

---

## Open questions for Yossi

1. **`{{scans_count}}` realism**: do we have a real, accurate "scans run during year" count? If not, this becomes vaporware. Falls back to "we monitored your plate ongoing" generic.
2. **Auto-renew default**: what's the actual product behavior at expiry — silent lapse, or auto-charge with opt-out? Affects whether C6 is "convert to paid" or "stop the auto-charge from being declined."
3. **Day-of (touch 4) for no-fines users**: are we sure we want to skip them? Counter-argument: a user who reaches expiry with no fines might convert on a clean "good year, let's keep it going" message. Worth testing on a slice (still no coupon — VIP isn't discounted here).
4. **Auto-renew with Detection vs VIP**: if user has Detection (₪99) and we want to upgrade to VIP, is that a "change plan + auto-renew at higher tier" flow that the bot should walk them through, or always a checkout-via-link?
