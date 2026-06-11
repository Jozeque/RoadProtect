# C4 — Trademobile Welcome (v2)

**Scenario code**: `C4`
**Channel**: WhatsApp, C2B outbound
**Audience**: New Trademobile customer who just purchased a car — auto-enrolled in 1 year free Detection
**Goal**: Activate the relationship, set the value of "protected in advance," create memory for the future first-fine moment
**Tone**: Warm, slightly celebratory, informative. **Zero hard sell.** This is the user's first impression — earn the right to message them again.

---

## Critique of current version (`06_bot/scenarios/c2b/04_trademobile_welcome.md`)

What's weak in the original:

1. **Two variants without a clear use rule.** Original has "official variant" and "front-loaded sell variant" and defaults to variant 1 — but the doc itself sounds unsure. Spec should pick one for v1 and put variant 2 in the A/B slot.
2. **No follow-up touch.** A welcome is the highest-engagement moment we will ever have with this user — and the original treats it as a one-shot. Even a "by the way, here's what we found in the first 30 days" check-in would compound trust.
3. **No timing relative to purchase event.** "Within 24h" is in the trigger comment but unspecified — is it immediately, 1 hour later, next morning?
4. **"רוב הנהגים עושים טעות ומתעלמים מדוחות"** in variant 2 is sales-y for a welcome moment. Welcome is not the place to call the user (or "average drivers") careless.
5. **Open question about "30 days post-welcome with stats"** — the answer is obviously yes, and it should be in the spec as touch 2.

What's strong (kept):

- The Trademobile relationship anchor (car purchase → free year)
- The "protected in advance" framing
- Calm tone, no urgency

---

## Trigger predicate

```
TRIGGER (C4):
  user.subscription = 'trademobile_free'
  AND user.subscription.started_at >= NOW() - INTERVAL '2 hours'   -- fired very fresh from purchase
  AND user.subscription.started_at <= NOW()
  AND user.opted_out = FALSE
  AND NOT EXISTS (any prior C4 event for this user)                -- C4 fires exactly once per user, lifetime
```

**C4 is single-fire per user — even if they buy a second car via Trademobile, that's a separate user/account flow, not a C4 re-trigger.**

---

## Variables used

- `{{name}}`
- `{{plate}}` — used in touch 2 ("the plate we've been watching")
- `{{plan_link}}` — UTM-tagged with `campaign=C4`
- `{{events_count}}` — used in touch 2 only; if zero, fall back to "kept watch — nothing bad found" variant

---

## Sequence

### Touch 1 — Welcome message

**Delay**: +2 hours from purchase event (give the dealership moment time to settle; user is no longer mid-paperwork)
**Variants**: A (default), B (Trademobile-co-branded variant for A/B)
**Skip conditions**: none
**Exit conditions**: continues to touch 2 regardless of reply (C4 is the only scenario where touch 2 fires on a calendar regardless of reply state — see § Special behavior)
**Events emitted**: `touch.sent`, `touch.delivered`, `touch.replied` (if user replies)

#### Variant A — Default welcome

```
היי {{name}}, כאן צוות Road Protect — ברכות על הרכב החדש! 🚗

עם הרכישה ב-Trademobile, חבילת ההגנה שלנו הופעלה אצלך אוטומטית, חינם לשנה שלמה. אין מה לעשות עכשיו — הכל כבר רץ ברקע.

מה אנחנו עושים בזמן הזה: סורקים 24/7 את מאגרי המשטרה וכ-20 עיריות. ברגע שנרשם דוח על שמך, נשלח התראה לוואטסאפ ולמייל — בדרך כלל לפני שהמכתב מהמשטרה מגיע אליך בכלל. זה ההבדל בין לערער בזמן לבין לשלם כפל קנס + ריבית של 50%.

יש שאלה? כתוב לי כאן. ואם הכל ברור — נסיעה בטוחה, אנחנו ברקע. 🛡️
```

#### Variant B — Trademobile co-brand reference (A/B test)

```
היי {{name}}, ברכות על הרכב מ-Trademobile! 🚗

כחלק מהעסקה, Road Protect מספק לך שנה שלמה של הגנה על דוחות — חינם, אוטומטי, כבר מהיום.

המערכת שלנו סורקת ברקע את מאגרי המשטרה והעיריות, ושולחת לך התראה ברגע שמופיע דוח על שמך. ככה אתה מגלה את הדוח לפני שהוא מצטבר לכפל קנס. הכל אצלך, אתה לא צריך לעשות כלום.

תרצה שנשלח לך סקירה קצרה של איך זה נראה בפועל? יש שאלה? כאן.
```

**Quality checklist (touch 1):**
- [x] Celebratory but not over-the-top
- [x] Brand identification in first 2 lines
- [x] Says what we do, not what we sell
- [x] Closes with "we're in the background" not a CTA
- [x] No VIP pitch. The user just bought a car — they're not in a buying mood today.
- [x] 4 paragraphs, gender-neutral, brand emoji + car emoji = 2 emojis max

---

### Touch 2 — Month-1 check-in (proof of value)

**Delay**: +30 days from touch 1 (calendar, not "if no reply")
**Variants**: A_no_fines, A_with_fines
**Skip conditions**: opted-out | C5 fired in the meantime (then C5 owns the conversation) | unsubscribed
**Exit conditions**: after sending → ends C4 sequence (user transitions to passive "covered" state; future engagement is via C5 / C6)
**Events emitted**: `touch.sent`, `touch.delivered`, optionally `touch.replied`, `sequence.completed`

#### Variant A_no_fines — "all clean, here's what we did"

```
היי {{name}}, חודש מאז שהצטרפת אלינו ב-Road Protect. ⏱

המערכת סרקה ברקע {{events_count}} פעמים את מאגרי המשטרה והעיריות עבור הרכב שלך ({{plate}}) — ובינתיים, הכל נקי. אין דוחות פתוחים על שמך.

ככה זה אמור להיות. אנחנו ממשיכים. אם משהו יוצץ — תקבל הודעה כאן מיד.

(ושאלה אחת אם מעניין: רוצה לראות איזה רשויות בדיוק אנחנו סורקים? אני זמין.)
```

If `events_count` data unavailable: fall back to "המערכת המשיכה לסרוק עבורך ברקע. בינתיים, הכל נקי..."

#### Variant A_with_fines — "we found one — and here's what we'll do about it"

```
היי {{name}}, חודש מאז שהצטרפת אלינו ב-Road Protect. ⏱

המערכת איתרה במהלך החודש {{events_count}} דוח/ות על שמך עבור הרכב {{plate}}. שלחנו לך התראה בזמן אמת — ככה זה אמור לעבוד.

הדוחות פתוחים. במסלול האיתור הנוכחי שלך, הטיפול עליך (ניסוח ערעור, הגשה לרשות, מאבק על הנקודות). במסלול VIP אנחנו לוקחים את כל זה על עצמנו.

תרצה לעבור על הדוח/ות שאיתרנו? נדבר כאן.
```

**Note**: variant A_with_fines is a soft VIP intro — but it's framed as "here's the next layer," not "you must upgrade." If the user doesn't reply, that's fine — C5 will fire on the *next* detected fine and pick up the conversation then.

---

## Branches (when user replies)

C4 is welcome — most replies are questions, not objections. Branches lean toward education.

### B1 — "What information do you have on me?"
```
מה שיש לנו: מספר רכב ({{plate}}), ת.ז. ושם — מה שנדרש כדי לסרוק את מאגרי הרשויות עבורך. הכל מאובטח בתקני אבטחת מידע, ולא נעשה שום שימוש אחר במידע מעבר לסריקה. רוצה לראות את ההגדרות?
```
**Event**: `branch.taken: data_question`

### B2 — "Which authorities do you scan?"
Per FAQ:
```
משטרת ישראל + מעל 20 עיריות, ביניהן תל אביב, ירושלים, חיפה, ראשון לציון, פתח תקווה, אשדוד, נתניה, באר שבע, חולון, בני ברק, רמת גן, אשקלון, רחובות, בת ים, הרצליה, כפר סבא, חדרה, מודיעין, נצרת, לוד, רעננה ועוד.
```
**Event**: `branch.taken: authorities_question`

### B3 — "What's the difference between this and VIP?"
Per FAQ + objection library:
```
איתור: סורקים, מתריעים, אתה מטפל בערעור.
VIP: סורקים, מתריעים, ומומחי הצוות שלנו מנסחים ומגישים את הערעור עבורך + סופגים ריבית פיגורים + מטפלים בתשלום מול הרשות אם צריך.
היום אתה במסלול האיתור — חינם לשנה. רוצה שאשלח לך את הפרטים על VIP, או שזה רלוונטי רק אם דוח מופיע?
```
**Event**: `branch.taken: tier_compare`

### B4 — "Are you a law firm?"
Canonical legal-line answer per objection library.
**Event**: `branch.taken: law_firm`

### B5 — "thanks" / quiet positive
```
בכיף — אנחנו כאן ברקע. נסיעה בטוחה. 🛡️
```
**Event**: `branch.taken: positive_ack`

### B6 — Opt-out
Per § 0.8. Note: opting out of C4 means opting out of *all* Road Protect outbound, including future fine alerts (which is bad for the user). Bot warns:
```
לפני שאני מוודא — אם תוסר מההתראות, גם הודעות על דוחות שיופיעו על שמך לא יישלחו. זה חבילת השירות החינמית שלך. עדיין להסיר?
```
If user confirms → opt-out per § 0.8. If user backs off → stay subscribed.

### B7 — Other
Fall to B1 inbound classifier.

---

## Special behavior

C4 is the **only scenario where touch 2 fires regardless of touch-1 reply state**. Reason: the month-1 proof-of-value beat is too valuable to skip, and a non-reply to touch 1 is normal (user just bought a car, may not be ready to engage). Touch 2 is *not* a nudge — it's a service moment.

C4 also **does not exhaust** — it completes. The state machine transition after touch 2 is `sequence.completed`, not `exhausted`, because we intentionally chose not to continue. Subsequent engagement comes via:
- C5 if a fine is detected
- C6 at month 11 (pre-expiry)
- C7 if user views a fine in-app and doesn't convert

---

## Suppression and exit

- **C5 fires between touch 1 and touch 2**: C5 takes the conversation. Touch 2 fires anyway at +30 days but uses variant A_with_fines based on detected count.
- **User cancels Trademobile / vehicle ownership change**: C4 ends, status `expired`.
- **Conversion to VIP during C4 window**: `converted`. Touch 2 still fires but as a "thanks for upgrading" check-in — variant A_just_upgraded (define if needed; for v1, fall back to A_no_fines).

---

## Events emitted

Standard, plus:
- `welcome.sent` — explicit event for funnel-start tracking (Trademobile-cohort cohort definition)
- `month_1_checkin.sent` — fires on touch 2 (powers the "did we activate this user?" cohort metric)
- `sequence.completed` — C4-specific, distinct from `exhausted`

---

## A/B testing slots

- **Variant A vs Variant B in touch 1** — default welcome vs Trademobile co-brand
- **Touch 2 month-1 check-in: with vs without VIP intro** — does it boost conversion or hurt the welcome feel?
- **Touch 1 timing: +2h vs +24h vs next-morning-9am** — test which converts to engagement

---

## Open questions for Yossi

1. **Trademobile co-brand**: do we have permission / contractual ground to invoke "Trademobile" by name in our messages? This is the cleanest A/B test if yes.
2. **Touch 1 timing**: original says "within 24h." My spec says +2h. Test or just decide?
3. **Touch 2 with A_just_upgraded variant**: write it for v1 or defer?
4. **Vehicle-change handling**: if user trades the car, do we update `{{plate}}` automatically or does C4 fire fresh? Affects the data feed.
