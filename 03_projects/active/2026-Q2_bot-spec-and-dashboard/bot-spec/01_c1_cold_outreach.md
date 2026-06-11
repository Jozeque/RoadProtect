# C1 — Cold Outreach (v2)

**Scenario code**: `C1`
**Channel**: WhatsApp, C2B outbound
**Audience**: Leads who submitted contact details previously and never subscribed (cold prospect, persona P3)
**Goal**: Re-introduce Road Protect, soft-diagnose whether they have a fine right now, open a real conversation
**Tone**: Warm, informative, low-pressure. The lead-frustration ratio here is high — they don't remember us. Don't act like we're old friends.

---

## Critique of current version (`06_bot/scenarios/c2b/01_cold_outreach.md`)

What's weak in the original:

1. **Single-touch.** One message, four reply branches. If the user doesn't reply, the sequence is dead — no second touch, no third. For a *cold* audience this is the absolute worst place to give up after one message; cold sequences in any drip platform are typically 3–5 touches.
2. **No exit criteria.** What stops the sequence? Implicitly "the user replies." But what if they don't? Currently undefined.
3. **No frequency cap stated.** The original asks "is there a frequency cap?" as an open question. Vendor needs an answer, not a question.
4. **AI disclosure buried in the closing line.** For cold, the AI disclosure should be unambiguous in touch 1 — otherwise we're flirting with deceptive practice in a market that increasingly cares about it.
5. **"היום כבר ממש לא חייבים לשלם דוחות 'על עיוור'"** — fine line, but for a cold lead it's a bit cute. We don't know what they care about yet. The hook should be the actual problem (lost mail / surprise fines), not the cute framing.
6. **Branches lack timing for the bot's response.** B3 ("not interested") says "single light follow-up" — when? Immediately? After a day? Vendor will guess.
7. **No event emission list.** Vendor has no idea what to instrument.

What's strong (kept):

- The "אם השארת אצלנו פרטים בעבר" framing is correct — it grounds the legitimacy of the outreach.
- Branch coverage is reasonable (pricing, "who are you", deflection).
- The statistic-based deflection-handler in B3 is good.

---

## Trigger predicate

```
TRIGGER (C1):
  user.status = 'lead'                                    -- has submitted details
  AND user.subscription IS NULL                           -- never subscribed
  AND user.created_at <= NOW() - INTERVAL '60 days'       -- not too fresh (avoid stepping on welcome flows)
  AND user.created_at >= NOW() - INTERVAL '2 years'       -- not too stale (no legitimate-interest claim past 24 months)
  AND user.last_outbound_at IS NULL OR user.last_outbound_at <= NOW() - INTERVAL '180 days'
  AND user.opted_out = FALSE
  AND user.phone IS NOT NULL AND user.phone_valid = TRUE
  AND NOT EXISTS (active C5/C7 or any scenario in 'entered' or 'replied' state for this user)
```

**Why these numbers:** 60 days lower bound = old enough that they've forgotten us; 2 years upper bound = consent-grounding requirement; 180-day re-contact cap = once per 6 months max for cold.

---

## Variables used

- `{{name}}` — `user.first_name`, fallback "שלום"
- `{{plan_link}}` — UTM-tagged: `?utm_source=whatsapp&utm_medium=bot&utm_campaign=C1&utm_content=<touch>&utm_term=<variant>`

---

## Sequence

### Touch 1 — Reintroduction + soft diagnostic

**Delay**: 0 (fires immediately on `eligible`)
**Variants**: A (default), B (problem-first)
**Skip conditions**: none (this is the entry)
**Exit conditions**: `replied` → branch logic | `opted_out` | `undeliverable`
**Events emitted**: `touch.sent`, `touch.delivered`, (if user replies) `touch.replied`

#### Variant A — Reintroduction (default)

```
היי {{name}}, כאן Road Protect — שירות ההגנה על נהגים בדרכים.

אני פונה כי השארת אצלנו פרטים בעבר, ורציתי לוודא שלא פיספסת מה שבנינו בזמן האחרון. אני סוכן AI דיגיטלי, ואני כאן לענות על כל שאלה.

המערכת שלנו סורקת ברקע את מאגרי המשטרה וכ-20 עיריות, ושולחת התראה לוואטסאפ ולמייל ברגע שנרשם דוח על שמך — לפני שמכתב יוצא בכלל בדואר. בלי זה, רוב הנהגים מגלים את הדוח כשהוא כבר הוכפל וצברה ריבית פיגורים של 50%.

האם יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא להיות מכוסה לפני שזה קורה? 🛡️
```

#### Variant B — Problem-first (for A/B)

```
היי {{name}}, רגע — לפני שאתה ממשיך את היום, שאלה קצרה.

קיבלת לאחרונה דוח שהפתיע אותך, או מכתב מהמשטרה שהגיע באיחור? כי זה בדיוק מה ש-Road Protect בונה כדי למנוע. אני סוכן AI דיגיטלי של השירות, ופוגש אותך כי השארת אצלנו פרטים בעבר.

אנחנו סורקים את מאגרי הרשויות 24/7 ומתריעים בוואטסאפ ובמייל ברגע שדוח נרשם — לפני שהוא הופך לכפל קנס.

האם זה רלוונטי עבורך עכשיו?
```

**Quality checklist (touch 1):**
- [x] Opens with personalized greeting
- [x] Identifies brand in line 1
- [x] AI disclosed in first paragraph
- [x] States reason for outreach ("השארת אצלנו פרטים בעבר")
- [x] Ends with diagnostic question
- [x] 4 paragraphs, gender-neutral
- [x] 1 emoji (Variant A)
- [x] No legal-line violations

---

### Touch 2 — Light nudge

**Delay**: +72h after touch 1
**Variants**: A (single)
**Skip conditions**: user replied at any point | converted | opted_out | escalated | suppressed by higher-priority scenario
**Exit conditions**: `replied` → branches | `opted_out` | continue to touch 3 if no reply
**Events emitted**: `touch.sent`, `touch.delivered`, (if reply) `touch.replied`

```
היי {{name}}, רק רציתי לוודא שההודעה הקודמת הגיעה.

חבל לפספס — נהג ממוצע בישראל מקבל 2 דוחות בשנה, וברוב המקרים גם לא יודע שהם נרשמו עד שמגיע מכתב עם כפל קנס בדואר.

האם יש משהו ספציפי שתרצה לבדוק, או שעדיף שאשלח לך פעם אחת קישור עם הפרטים? [link={{plan_link}}]
```

**Why this works:** acknowledges silence without guilt-tripping, repeats the core stat the user might have missed, offers two low-friction options (talk or just-send-link).

**Quality checklist (touch 2):**
- [x] Light tone, no urgency stacking
- [x] One stat (2-fines-a-year), no invented numbers
- [x] 3 short paragraphs
- [x] Question + link offered

---

### Touch 3 — Final value reframe, soft door-close

**Delay**: +5 days after touch 2 (so ~8 days from touch 1)
**Variants**: A (single)
**Skip conditions**: same as touch 2
**Exit conditions**: after sending → `exhausted` (no further outbound for 180 days)
**Events emitted**: `touch.sent`, `touch.delivered`, `sequence.exhausted` (after a 24h grace window with no reply)

```
היי {{name}}, ההודעה האחרונה ממני בסבב הזה — אני לא רוצה להציק.

הסיבה שבחרנו לפנות אליך היא שבמהלך 2026 הרפורמה בתעבורה משנה את כל המסלול של ערעורים. דוחות הופכים להליך מנהלי, וטעות בניסוח הערעור עלולה לעלות באלפי שקלים ובנקודות. זה בדיוק הרגע להיות מוגן.

אם תרצה לבדוק מה רלוונטי עבורך — הקישור כאן: {{plan_link}}

ואם בכלל לא מעניין — אין בעיה. רק תכתוב לי "הסר", ואני מוודא שלא נחזור.
```

**Why this works:** the 2026 reform is the strongest external tailwind we have; it gives a *real reason* this message arrived now (not just "wanted to follow up"). The "הסר" prompt is intentional — invitation to opt-out reduces complaint risk and signals respect.

**Quality checklist (touch 3):**
- [x] Acknowledges this is the last touch
- [x] Real reason (2026 reform) — not invented urgency
- [x] Link + opt-out CTA explicit
- [x] Tone: respect, not desperation

---

## Branches (when user replies to any touch)

### B1 — User asks about a specific fine
**Routing**: hand off to the appeals department — **do not collect fine details here** (the appeal flow asks for them; re-collecting burns the user across two chats — Yossi, 25/04).

**Bot reply (Hebrew):**

```
אל תשלם/י לפני שתבדוק/י! המומחים שלנו במחלקת הערעורים יבחנו את הדוח וימקסמו את סיכויי ביטול הקנס והנקודות עבורך תוך כמה דקות. כדי להתחיל, פשוט שלח/י 'היי' למחלקת הערעורים כאן: {{appeals_link}}
```

**Event**: `branch.taken` with `branch = 'fine_specific'`

---

### B2 — User asks about pricing
**Bot reply:** *Don't surface pricing immediately.* Diagnostic first.

```
שאלה טובה — נעבור עליה בדיוק. רק כדי להתאים את המסלול הנכון: יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא הגנה כללית קדימה?
```

If user answers "future protection" → pitch Detection (₪99/year).
If "have a fine now" → pitch one-off (₪49) or VIP (₪489) based on signals.
If "both" → VIP.

**Event**: `branch.taken` with `branch = 'pricing_question'`

---

### B3 — User pushes back (not interested / no need)
**First response** (single light deflection):

```
אין בעיה. רק כדי שזה לא יפתיע אותך בעתיד — נהג ממוצע מקבל 2 דוחות בשנה, ובמעל 60% מהמקרים המכתב מגיע אחרי תאריך התשלום. רוב הנהגים מגלים על דוח דרך הריבית, לא דרך הדוח עצמו. מוזמן לחזור אלינו אם הסיפור הזה ייגע אותך — ועד אז, נסיעה בטוחה. 🛡️
```

**After this response**: emit `sequence.exhausted` (do not continue to touch 2/3 for this user — they explicitly said no).

**Event**: `branch.taken` with `branch = 'deflection'`, then `sequence.exhausted`

---

### B4 — User asks "who are you"
```
אני העוזר הדיגיטלי של Road Protect — שירות ההגנה בדרכים שמנטר עבור נהגים דוחות וריביות פיגורים בזמן אמת, ועוזר לערער עליהם. אני סוכן AI, ואפשר לשאול אותי הכל. 🛡️
```

**Event**: `branch.taken` with `branch = 'identity_check'`

---

### B5 — User opts out
Trigger phrases per `00_overview.md` § 0.8.

**Bot reply** (canonical opt-out ack):

```
הוסרת מרשימת התפוצה. לא נשלח אליך הודעות נוספות. אם תרצה לחזור — תמיד אפשר ליצור קשר בכתובת [link].
```

**Event**: `opted_out` with `reason = 'user_request'`

---

### B6 — User sends abusive / legal-threat content
Per `00_overview.md` § 0.12 — escalate. Bot sends canonical handoff message, status → `escalated`, page human team.

**Event**: `escalated` with `reason = 'legal_threat'` or `'abusive'`

---

### B7 — User reply doesn't match any branch
Fall back to B1 inbound intent classifier. Bot's response is whatever B1 routes to.

---

## Suppression and exit

- If a higher-priority scenario fires (C5 — user got a new fine while in C1 sequence): **C1 pauses**. Resume only if C5 closes without conversion AND C1's next touch is still within its valid timing window.
- If the user opts out: all sequences cancelled.
- If user converts (via this scenario's `{{plan_link}}` UTM): sequence exits with `converted`. No more touches.
- After touch 3 + 24h grace with no reply: `exhausted`. No new C1 outreach to this user for 180 days.

---

## Events emitted in this scenario

| Event | Touch | Payload notes |
|---|---|---|
| `scenario.eligible` | — | At trigger evaluation |
| `scenario.suppressed` | — | If suppression matrix blocks |
| `touch.sent` | 1, 2, 3 | `variant = A/B` |
| `touch.delivered` | 1, 2, 3 | from WhatsApp receipt |
| `touch.read` | 1, 2, 3 | from WhatsApp read receipt (if available) |
| `touch.replied` | 1, 2, 3 | with `reply_text` (full text, for the dashboard's reply-sampling view) |
| `branch.taken` | replied touch | `branch ∈ {fine_specific, pricing_question, deflection, identity_check, abusive, legal_threat, other}` |
| `objection.raised` | replied touch | when reply matches `objection_library.md` keys |
| `converted` | any | with `plan ∈ {detection, vip, one_off}`, `revenue_ils`, `touch_attributed_to` |
| `opted_out` | any | with `reason` and `trigger_phrase` |
| `sequence.exhausted` | after touch 3 | with `last_touch_at` |
| `bad_feedback` | replied touch | if reply matches bad-feedback signal (§ 0.16) |

---

## A/B testing slots

- **Touch 1 variant A vs variant B** — reintroduction vs problem-first opening
- **Touch 2 with vs without the link** — does adding the link in touch 2 boost conversion or kill replies?
- **Touch 3 with vs without the explicit "הסר" prompt** — does inviting opt-out reduce conversions, or only reduce complaints?

Vendor instruments these as variant tags on `touch.sent` events. Dashboard slices funnel by `variant`.

---

## Open questions for Yossi

1. **Cold list source**: are we re-engaging the *entire* historical lead list, or just leads where source ∈ {trademobile-not-converted, landing-page-form, partner-referral}? Affects volume forecasting.
2. **180-day cooldown**: too conservative? Too aggressive? Default to 180 unless Yossi calls otherwise.
3. **Trademobile-warm leads**: should we route these to C4 (welcome) instead of C1 (cold)? Currently C4 is post-purchase only — clarify.
4. **Variant B's "רגע — לפני שאתה ממשיך"**: feels good but pattern-interrupts. Test cautiously; could increase opt-out.
