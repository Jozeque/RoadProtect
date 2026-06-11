# Spec 1 — The Bot Scenarios (plain language)

*A simple tour of every conversation our WhatsApp bot has: who it's for, what we want, and how it gets there. The full build-ready version lives in `../bot-spec/`. This doc is the "what & why" in plain words.*

---

## The setup — two bots, one personality

- **Outbound bot ("we reach out first")** — 7 scenarios (C1–C7). We message a person at a specific moment in their life with us (just bought a car, got a fine, free year ending, started an appeal and stopped, etc.).
- **Inbound bot ("they message us first")** — 1 entry flow (B1) that figures out what the person wants and sends them the right way.

Both are the same AI agent, with the same voice and the same rules. They share one knowledge base.

---

## The golden rules (true in every scenario)

1. **Say who we are, up front.** "כאן צוות Road Protect." People who get a fine alert often think it's the municipality. Remove that confusion immediately.
2. **Empathy → urgency → sale.** Acknowledge the annoyance ("איזה באסה") before pitching anything.
3. **One clear ask per message,** and end with a question so the conversation keeps moving.
4. **Gender-neutral until we know.** Start neutral ("עבורך / שלך"), and once their first reply reveals gender, mirror it. The bot never guesses a name or gender.
5. **The legal line.** We are **not** a law firm. Allowed: "מומחים", "נלחמים בשבילך", "מנסחים את הערעור בשמך". Never: "עורכי דין שייצגו אותך", "מבטיחים ביטול". We maximize the *chances* of cancellation — we don't promise it.
6. **Admit we're an AI when asked.** "אני סוכן AI דיגיטלי."
7. **The coupon rule** (see below) — one coupon, one purpose.
8. **Trademobile = a car purchase, never "leasing."** Name the partner, and frame the free year as "השירות שקיבלת מטרייד מוביל."
9. **Appeals go to the appeals desk.** When someone wants to appeal, send them straight to the appeals WhatsApp (052-586-6982) — don't re-collect the fine details in the sales chat (they'll just type the same thing twice and give up).

---

## The one coupon rule

One code: **SAVE30 = 30% off a single appeal (₪49).** It goes out **only** to people who started an appeal and didn't finish (scenario C7). **Never** on VIP, **never** 50%, **never** "pick your discount." We convert **gradually**: close the cheap appeal first so they experience the system, then offer VIP later in a separate conversation. Cold leads and people with no fines get **no coupon** — VIP is already cheap.

---

## The 7 outbound scenarios

### C1 — Cold outreach
- **Who:** old leads who left details but never subscribed (private / ad, not partners).
- **What we want:** re-introduce ourselves and find out if they have a fine right now.
- **The bot says (opener):** "היי {{שם}}, כאן Road Protect — שירות ההגנה על נהגים בדרכים. אני פונה כי השארת אצלנו פרטים בעבר... יש דוח פתוח שצריך לטפל בו עכשיו, או שהמטרה היא להיות מכוסה לפני שזה קורה?"
- **Note:** low pressure, no coupon, says it's an AI in the first message. If they have a fine → straight to the appeals desk.

### C2 — Trademobile free-year user with fines
- **Who:** someone on the free Trademobile year who already has detected fines.
- **What we want:** upgrade them to VIP so we actually handle the fines.
- **The bot says:** "...עם רכישת הרכב בטרייד מוביל קיבלת מאיתנו שנת ניטור והתראות, ובתקופה הזו איתרנו עבורך {{כמות}} דוחות..."
- **Note:** must name Trademobile and use the real fine count.

### C3 — Past-customer win-back
- **Who:** someone whose paid plan lapsed, and we've found new fines since.
- **What we want:** reactivate them on VIP.
- **The bot says:** "הצטרפת אלינו בעבר, ואחרי שהמינוי נגמר המערכת המשיכה לסרוק ברקע. מאז שעזבת איתרנו {{כמות}} דוחות פתוחים..."
- **Note:** acknowledge the history without guilt-tripping. **No coupon** — we close on value, not a discount.

### C4 — Trademobile welcome (new car buyer)
- **Who:** someone who just bought a car via Trademobile (= just got the free year).
- **What we want:** welcome them, make the free protection feel valuable, set up a later upsell.
- **The bot says:** "ברכות על הרכב החדש! עם רכישת הרכב בטרייד מוביל, חבילת התראות וניטור דוחות לשנה שלמה כבר מחכה לך — ללא עלות..."
- **Note:** celebratory, no hard sell in the first message.

### C5 — Free user just got a fine (real time)
- **Who:** a free/Detection user the moment our radar finds a new fine.
- **What we want:** empathy first, then push to VIP so experts handle the appeal.
- **The bot says:** "כאן צוות Road Protect 🛡️ איתרנו עבורך דוח חדש ⚠️ איזה באסה!... רגע לפני שרצים לשלם — שווה לעצור..."
- **Note:** this is the highest-intent moment we have. Identify ourselves first (they may think it's the city).

### C6 — Free year about to end
- **Who:** Detection / Trademobile-free users ~30 days from expiry (then 14 / 3 / day-of).
- **What we want:** convert to paid before the protection switches off.
- **The bot says:** "חודש מהיום ההגנה החינמית שלך מסתיימת. השנה סרקנו עבורך {{כמות}} פעמים ואיתרנו {{כמות}} דוחות..."
- **Note:** lead with proof of value, then what they'd lose. **No coupon.**

### C7 — "Dirty & quick": abandoned appeal (the only coupon scenario)
- **Who:** someone who started a single appeal and didn't finish.
- **What we want:** get them to **finish that appeal** with 30% off. (VIP comes later.)
- **The bot says:** Touch 1 (no coupon): "ראיתי שהתחלת תהליך ערעור ולא סגרנו את זה. רוצה שנסיים?" → Touch 2 (coupon): "סידרתי לך 30% הנחה על הערעור הנוכחי — הקוד SAVE30."
- **Note:** never "the fine we detected for you" (they brought their own fine) — say "the appeal you started."

---

## The inbound bot

### B1 — Someone messages us first
- **Who:** anyone — subscriber, prospect, lapsed, curious.
- **What we want:** figure out what they need in 1–2 messages and route them.
- **How it routes:** Got a fine → straight to the appeals desk (no detail collection). What is this / are you lawyers → short explainer + the legal line. How much → ask "fine now or future protection?" then the right plan. Cancel / change plan → email info@roadprotect.co.il. Company fleet → "our CEO will be in touch." Wants a human → hand off.

---

## What we want to achieve overall

A bot that feels like a sharp human teammate: it knows who you are, talks to you correctly (right gender, right fine count, right partner), creates real urgency without lying, never promises what it can't deliver, and always knows the next right step. That's what turns a cold WhatsApp message into a paying customer.

---

## Out of scope (for this round)

- New scenarios beyond these 8 (they go through the normal idea → spec pipeline).
- B2B partner messaging (Pango, Strauss, etc.) — that's partner-side, separate.
- Email / SMS — WhatsApp only this round.
