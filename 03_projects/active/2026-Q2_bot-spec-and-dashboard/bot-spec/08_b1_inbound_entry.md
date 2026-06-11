# B1 — B2C Inbound Entry (v2)

**Scenario code**: `B1`
**Channel**: WhatsApp, B2C inbound
**Audience**: Anyone — subscriber, prospect, lapsed, cold — who initiates a WhatsApp conversation with Road Protect
**Goal**: Quickly classify intent → route to the right sub-flow → resolve or escalate
**Tone**: Helpful, friendly, neutral until intent is known. The user came to us — don't pitch before understanding.

---

## Critique of current version (`06_bot/scenarios/b2c/01_inbound_entry.md`)

What's weak in the original:

1. **Intent taxonomy is implicit, not explicit.** The original lists "Intent 1, 2, 3, 4" with example user inputs but doesn't define how the bot *classifies* — keyword matching? LLM intent classifier? Vendor must guess.
2. **No fallback for unrecognized intents.** If the user says something the bot doesn't recognize, what happens? Currently undefined.
3. **No multi-turn diagnostic flows.** Intent 1 is "I got a fine, I don't know what to do" — the bot's response asks for "when received, what violation, amount" but doesn't specify *the loop* (what if user gives only the amount? does it ask again?).
4. **B1 has no relation to the C2B sequences.** A user who's mid-C5 might message inbound — does B1 reuse C5's branches, or does it route generically? Currently undefined.
5. **No event emission for inbound classification.** Dashboard can't tell which intents are most common.
6. **"Don't pre-pitch a plan before knowing"** is the right principle but only the price intent enforces it — the fine-intent answer is already pre-pitching VIP.

What's strong (kept):

- Variant A (slightly guided) is the right default — keep it
- The four canonical intents are the right initial taxonomy
- "Question back, never monologue" principle

---

## Trigger predicate

B1 is **always-on** — fires on every inbound message from any user to the Road Protect WhatsApp number.

```
TRIGGER (B1):
  message.direction = 'inbound'
  AND message.channel = 'whatsapp'
  AND (
    user_session.b1_active = FALSE                            -- new conversation
    OR message.received_at - user_session.last_message_at > INTERVAL '12 hours'   -- session expired, treat as new
  )
  AND user.opted_out = FALSE
```

If user has opted out and messages in: bot responds with re-onboarding message (per § Re-onboarding below), does **not** auto-resubscribe.

---

## Intent taxonomy

B1 must classify every inbound message into exactly one intent. Eight intents in v1:

| Intent ID | Name | Description | Trigger phrases (samples) |
|---|---|---|---|
| `I1_fine_received` | Got a fine, needs help | User has a specific fine and wants to know what to do | "קיבלתי דוח", "יש לי קנס", "מה לעשות עם דוח" |
| `I2_what_is_this` | What is Road Protect | Curiosity, doesn't know us | "מה זה", "מה אתם עושים", "אתם משרד עו"ד" |
| `I3_pricing` | Wants to know cost | Pricing-focused | "כמה זה עולה", "מחיר", "כמה?" |
| `I4_how_does_detection_work` | Wants to understand the radar | Detection mechanism question | "איך אתם יודעים", "איך הסריקה", "איזה רשויות" |
| `I5_account_question` | Subscriber account issue | Existing subscriber, account-specific | "המינוי שלי", "חיוב", "ביטול", "החלפת רכב" |
| `I6_appeal_status` | Status of in-flight appeal | VIP user asking about ongoing case | "מה קורה עם הערעור", "התקדמות", "סטטוס דוח" |
| `I7_complaint` | Complaint or bad feedback | Anger, frustration, demand to stop | "מעצבן", "ספאם", "תפסיקו" |
| `I8_human_request` | Wants to talk to a person | Explicit ask | "נציג", "בן אדם", "מישהו אמיתי" |
| `I9_fallback` | Couldn't classify | Default if no match | (anything else) |

**Classification mechanism** (vendor choice, with priority order):

1. **Phrase-match first** — match against trigger-phrase list per intent. Hits → assign that intent.
2. **LLM classifier second** — if no phrase match, vendor's LLM classifies into the 8 intents. Confidence threshold ≥ 0.7 for assignment.
3. **Fallback to `I9_fallback`** — if LLM confidence < 0.7.

**Multi-intent handling**: if user message contains two intents (e.g., "What does it cost and do you guys cancel fines?"), classify by the *primary* intent the user is most likely to want addressed. Heuristic: pricing wins over feature questions.

---

## Opening message (when user first messages in)

The bot's first response when `user_session.b1_active = FALSE`:

```
היי! תודה שפנית ל-Road Protect 🛡️

קיבלת דוח שאתה רוצה לטפל בו, או שתרצה להבין מה אנחנו עושים? אני סוכן AI דיגיטלי ופה כדי לעזור. אם תכתוב לי בקצרה מה הסיפור, אדע להפנות אותך נכון.
```

**Why this works:**
- Brand identification immediately
- AI disclosure in the first message (different from C2B which can be cold) — the user reached out, they should know who they're talking to
- Two paths (fine handling / info) — gives an anchor
- Open-ended close — invites context

**If the user's first message already contains classifiable intent** (e.g., they opened with "כמה זה עולה"): **skip the opener and route directly** to the relevant intent. Don't make the user wait through a generic greeting when they've already told us what they want.

---

## Per-intent sub-flows

### I1 — Fine received

**Bot reply** (route to appeals — do NOT collect fine details here):
```
טוב שפנית לפני שביצעת תשלום! דוח שלא מטופל בזמן עלול לצבור ריבית פיגורים של 50% וכפל קנס, אז ממש שווה לבדוק לפני שמשלמים.

אל תשלם/י לפני שתבדוק/י — המומחים שלנו במחלקת הערעורים יבחנו את הדוח וימקסמו את סיכויי ביטול הקנס והנקודות עבורך. כדי להתחיל, פשוט שלח/י 'היי' למחלקת הערעורים כאן: {{appeals_link}}
```

> ⚠️ **Don't collect fine details in this chat.** Route the user straight to the appeals department (WhatsApp **052-586-6982**). The appeal flow itself asks for the details — if B1 also collects them, the user enters the same info twice across two WhatsApp conversations and gives up (Yossi, 25/04). The conversion agent hands off to appeals cleanly; it doesn't run the appeal intake.

**Events emitted**: `b1.intent: fine_received`, `branch.taken: routed_to_appeals`

---

### I2 — What is Road Protect

**Bot reply:**
```
אנחנו שירות שעוזר לנהגים בישראל להתמודד עם דוחות תנועה. שלוש שכבות:

1. **רדאר** — סורקים 24/7 את מאגרי המשטרה וכ-20 עיריות אחר דוחות שנרשמים על שמך.
2. **התראות** — ברגע שמופיע דוח, נשלח התראה לוואטסאפ ולמייל — לרוב לפני שמכתב בכלל יוצא בדואר.
3. **טיפול** — המומחים שלנו במסלול VIP מנסחים את הערעור בשמך כדי לבטל את הדוח והנקודות.

לא משרד עורכי דין — כלי דיגיטלי שעוזר לך לנהל את הסיפור.

יש לך דוח עכשיו, או שזה לבירור כללי?
```

**Events**: `b1.intent: what_is_this`, route to next intent based on user's reply.

---

### I3 — Pricing

**Bot reply (don't surface plans immediately — diagnostic first):**
```
שלוש אופציות במחיר. כדי להתאים — שאלה אחת קודם: יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא הגנה כללית לעתיד?
```

**Branching based on reply:**

- **"יש דוח עכשיו"** → ערעור נקודתי (₪49 — וירוסיב פעמי) או VIP (₪489/שנה — אם זה דפוס).
- **"הגנה כללית"** → איתור (₪99/שנה) או VIP (₪489/שנה — אם רוצה גם טיפול בערעורים).
- **"שתיהן"** → VIP.

**Full plan summary** (sent when user asks for "all options"):
```
שלושה מסלולים:
• **איתור** — ₪99/שנה (₪8.25/חודש). רדאר + התראות, הטיפול עליך.
• **VIP** — ₪489/שנה (₪40.75/חודש). הכל באיתור + ערעורים בלתי מוגבלים על ידי המומחים + ספיגת ריבית פיגורים + הפניה לעו"ד אם צריך.
• **ערעור נקודתי** — ₪49 חד פעמי. ערעור על דוח אחד, ללא הגבלת זמן לניצול.

איזה הכי מתאים לסיטואציה שלך?
```

**Events**: `b1.intent: pricing`, `branch.taken: <one_off|detection|vip|undecided>`

---

### I4 — How does detection work

**Bot reply:**
```
המערכת מחוברת למאגרי המידע הרשמיים של המשטרה וכ-20 עיריות (תל אביב, ירושלים, חיפה, ראשון לציון, פתח תקווה, אשדוד, נתניה, באר שבע, חולון, בני ברק, רמת גן, אשקלון, רחובות, בת ים, הרצליה, כפר סבא, חדרה, מודיעין, נצרת, לוד, רעננה, ועוד).

הסריקה רצה ברקע 24/7. ברגע שדוח נרשם על השם שלך — האיתות קופץ אצלנו, ושולחים התראה לוואטסאפ ולמייל. בדרך כלל זה קורה תוך דקות עד שעות מרגע הרישום ברשות.

ככה אתה יודע על הדוח לפני שמכתב חוזר בדואר (וזה הזמן שבו אפשר עוד לערער ביעילות).

יש שאלה ספציפית או רוצה לבדוק אם יש דוח על שמך?
```

**Events**: `b1.intent: how_detection_works`

---

### I5 — Account question (subscriber-specific)

**Bot reply:**
```
שאלת חשבון. אני יכול לעזור עם חלק מהדברים, אבל כדי לזהות אותך — כתוב בבקשה את מספר הטלפון או הת.ז. שרשומים אצלנו, ואני אשלוף את החשבון שלך.
```

**Events**: `b1.intent: account_question`

**After authentication** → branch by sub-intent:
- "ביטול מינוי" → escalate to retention specialist (human)
- "חיוב לא צפוי" → escalate to billing (human)
- "החלפת רכב" → walk through plate update self-service if available, else escalate
- "מתי המינוי שלי נגמר" → bot can answer from account data

**For any sub-intent the bot cannot self-serve**: escalate per § 0.12.

---

### I6 — Appeal status (VIP subscriber)

**Bot reply:**
```
תרצה לבדוק את הסטטוס של ערעור פעיל. אני אעביר אותך לצוות שמטפל בערעור שלך כדי שיענו לך בדיוק — בדרך כלל תוך [N] שעות בשעות הפעילות.

בינתיים, אם יש לך עוד שאלה — אני כאן.
```

**Always escalate** per § 0.12 — bot doesn't have visibility into appeal status.

**Events**: `b1.intent: appeal_status`, `escalated: appeal_status_inquiry`

---

### I7 — Complaint / bad feedback

**Bot reply:**
```
אני מצטער על התסכול. רוצה שאסביר מה קורה, או שתעדיף לדבר עם נציג?
```

**Always flag**: emit `bad_feedback` event (per § 0.16) regardless of next step.

**If user says "תעדיף לדבר עם נציג"** → escalate.
**If user says "תסביר"** → contextual explanation based on previous messages (e.g., "You messaged because we sent you too many touches — I see, let me reduce frequency"), then offer either escalation or a soft re-engage.

**Events**: `b1.intent: complaint`, `bad_feedback` (with reply text in payload)

---

### I8 — Human request

Per `00_overview.md` § 0.12. Canonical handoff message:
```
בכיף — אני מעביר אותך לנציג. הם יחזרו אליך בהקדם, ובינתיים אני כאן אם יש משהו אחר.
```

**Always escalate**, no exceptions.

**Events**: `b1.intent: human_request`, `escalated: explicit_request`

---

### I9 — Fallback (no classification)

**Bot reply** (one clarification attempt):
```
אני לא בטוח שהבנתי לאשורו — תוכל לכתוב בכמה מילים על מה רצית לדבר? אם תרצה, אני יכול גם להעביר אותך לנציג שיענה.
```

**If second message also unclassifiable** → escalate per § 0.12 rule 9 (repeated misunderstanding).

**Events**: `b1.intent: fallback`, after 2nd miss → `escalated: repeated_misunderstanding`

---

## Re-onboarding (opted-out user messages in)

If a user with `opted_out = TRUE` sends a message:

```
היי! לפני שנמשיך — אתה רשום אצלנו כמי שביקש לא לקבל הודעות מאיתנו. רצית לחזור לקבל את ההגנה והעדכונים שלנו?

אם כן — תכתוב "כן". אם רק שאלה חד פעמית — אני אענה כאן, ולא נרשום אותך מחדש.
```

If user says "כן" → flip `opted_out = FALSE`, emit `re_subscribed` event.
If user asks a question without explicit re-opt-in → answer it but don't re-subscribe.

---

## Cross-scenario coordination

A user who is mid-C2B sequence and messages inbound: **B1 handles the conversation**, and the relevant C2B sequence's branches inform the response.

Specifically:
- If user is `entered` in C5 and messages with intent `I1_fine_received` → B1 routes them through C5's branches (using C5 copy), not the generic B1 fine-received flow. The dashboard shows this conversation under both B1 and C5 (joined by `correlation_id`).
- If user is in C7 and messages with intent `I3_pricing` → B1 surfaces the active appeal coupon (`SAVE30`, 30% off the ₪49 appeal — there is no other code) instead of full-price options.

**Implementation**: vendor maintains a single conversation state per user. Inbound messages re-enter that state, don't start a parallel session.

---

## Events emitted

| Event | When |
|---|---|
| `b1.session_started` | First inbound message of a new session |
| `b1.intent: <intent_id>` | After classification |
| `b1.data_collected: {fields}` | After multi-turn data gathering (intent I5 account auth) |
| `branch.taken: <branch_id>` | Specific sub-flow taken |
| `escalated: <reason>` | Per § 0.12 |
| `converted` | If conversation ends with conversion (link clicked + checkout completed) |
| `bad_feedback` | Per § 0.16 |
| `b1.session_ended` | After 12h with no further messages OR user explicit "תודה, סיימנו" |
| `re_subscribed` | If opted-out user re-opts in via B1 |

---

## Quality bar

- Bot must classify intent within first 2 inbound messages
- For a fine-received intent (I1), bot routes straight to the appeals department — it must NOT collect fine details or push a plans link (the appeal flow handles intake)
- Bot must escalate within 1 turn for any intent in {I5_account_question (non-self-serve), I6_appeal_status, I7_complaint, I8_human_request}
- Bot must disclose AI identity if asked
- Bot's first response in any session must include `🛡️` brand emoji at least once

---

## A/B testing slots

- **Opener variant A vs B** — guided ("got a fine or info?") vs minimal ("how can I help?")
- **Pricing intent diagnostic** — diagnostic-first vs surface-plans-first
- **Complaint intent (I7)** — bot apology + offer-to-explain vs bot direct-to-human-handoff

---

## Open questions for Yossi

1. **Intent classifier choice**: phrase-list + LLM, or LLM-only? Phrase list is cheaper / more predictable. Vendor's stack might prefer LLM-only.
2. **B1 in opt-out re-onboarding**: my spec auto-respects opt-out + asks for re-opt-in. Some platforms might require a different consent flow under WhatsApp Business policies. Confirm.
3. **Confidence threshold for I9 fallback**: 0.7 feels right but worth tuning post-launch based on misclassification rates from dashboard.
4. **Account auth flow**: my spec says "phone or ת.ז." for auth — is that sufficient identity verification per Road Protect's data handling, or do we need stronger (e.g., last 4 digits of payment method)?
