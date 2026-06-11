# Spec 3 — The Dashboard: What We Want to See (plain language)

*The numbers we need to run and improve the bot. The exact metric formulas and screen layouts are in `../dashboard-spec/`. This doc is the plain-language "what we want and why."*

---

## The problem

Today we're blind at the macro level. We can read individual WhatsApp chats one by one, but we **can't** answer the question that actually matters: *"Of everyone we messaged this week, how many replied, how many bought, and where did it break?"* Without that, we can't improve the bot, can't price-test the coupon, and can't justify sending more messages. (Yossi, 11/05: "we have to measure at the macro level, not per conversation.")

---

## What we want to see — the daily snapshot

The first thing on screen, every day, at a glance:

- **Conversations started today**
- **Messages sent** / **people reached** (delivered to WhatsApp)
- **People who engaged** (replied at least once)
- **Conversions** (completed a payment)
- **Conversion rate** = conversions ÷ reached
- **The drop-off at each step**: reached → replied → converted (the "X out of total reached" at every stage)

Plain definitions so we all mean the same thing:
- **Reached** = the message was delivered.
- **Engaged** = they replied at least once.
- **Converted** = they actually paid.

---

## Per scenario

For each of C1–C7 and the inbound bot, the same funnel:

- How many we **reached**
- **Reply rate to message 1, message 2, and message 3** (the message-2 number is one Yossi specifically asked for — does the nudge work?)
- **Conversion rate**, and **which message closed it** (so we know if we can shorten a sequence or where to fix the copy)
- **Revenue** from that scenario

---

## By cohort (which group is worth the most)

Compare the big groups side by side — **Trademobile vs cold leads vs lapsed vs free-with-a-fine** — on the same funnel. This tells us which audience converts best per message, so we point our volume where it actually pays off.

---

## The coupon view (C7 only)

- How many **SAVE30** codes were **issued vs redeemed**
- **Share of appeal conversions that needed the coupon** — a guardrail: keep it under ~25%, otherwise we're training people to wait for a discount instead of paying full price.

---

## The quality / guardrail view (is the bot behaving?)

- **Opt-outs** — and who (names).
- **Bad feedback** — "remove me," complaints, anger — with names **and the exact text they sent**.
- **Escalations to a human** — how often, and why.
- **Top objections this month** — what's stopping people from buying.

If opt-outs or bad feedback spike on a scenario, that scenario's copy or cadence is wrong — and the dashboard should flag it on its own.

---

## The "who" lists (click a number, see the people)

Every number should be clickable down to the actual people behind it:
- Who replied to message 1
- Who opted out
- Who gave bad feedback (with what they wrote)

Each row: name, phone, which scenario, what they said. This is how we learn and how we follow up by hand when it matters.

---

## The four screens

1. **Overview** — the daily snapshot + a "**what needs my attention**" strip (any scenario breaching a guardrail, any reply rate dropping).
2. **Scenario funnel** — pick a scenario, see reached → replied (per message) → converted, plus revenue.
3. **Cohorts** — compare Trademobile / cold / lapsed / etc.
4. **Conversations & quality** — the people lists, opt-outs, bad feedback, and top objections.

---

## What we want to achieve

When Yossi opens the dashboard, he can answer — unaided — all six of these:

1. How many we reached, by scenario, last 7 days.
2. Reply rate for message 1 / 2 / 3, per scenario.
3. Conversion rate per scenario, and which message closed it.
4. Who flagged bad feedback or asked to cancel (with names).
5. Which cohort converts best (Trademobile vs cold vs lapsed).
6. Top objections in the last 30 days.

With those answers we can tune the copy, price-test the coupon, and confidently turn the volume up — instead of guessing. **That's what makes it the best bot we can run.**

---

## What we don't need yet (out of scope)

- **Logins / permissions** — it's the internal team for now.
- **Real-time alerts** on metric anomalies — a clear daily view first.
- **Email / SMS tracking** — WhatsApp only this round.
