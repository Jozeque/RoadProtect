# Spec 2 — The Data Behind the Bot (plain language)

*What we know about each person, where it comes from, and how each fact changes the conversation. The technical field-by-field contract is in `../bot-spec/10_crm_integration.md`. This doc is the plain-language version.*

---

## What we have — one row per person

Our internal admin (the CRM) holds a row for every user. The bot reads it **live, just before every message**, so it always talks from the latest truth. The fields that actually drive the conversation:

| What we know | What it tells us | How the bot uses it |
|---|---|---|
| **Name** | who they are | personalize the greeting (never guess) |
| **Phone** | their WhatsApp identity | who to message |
| **Source / "root"** | how they came to us: Trademobile / private / paid ad / Pango / unknown | picks the scenario and the wording |
| **Current plan** | paying (Detection or VIP) / free Trademobile year / one-off appeal / none / lapsed | the single biggest routing lever |
| **Active fines (count)** | how many open fines we found | creates urgency; the real number goes in the message |
| **Last fine date** | when the most recent fine landed | lets us message right after a fresh fine |
| **Appeal stage** | none / just started / details filled / submitted / rejected / approved / closed | tells the bot whether to push, stay quiet, or be gentle |
| **Plan end date** | when the (free or paid) plan expires | drives the "your year is ending" flow |
| **Days since we last talked** | recency | how warm they are, and frequency limits |
| **Sentiment** | are they happy / neutral / upset (the bot fills this in from replies) | softens or stops pushy messages |
| **Churn risk & customer value** | how likely to leave, how much they're worth | how hard to push, when to back off |

The bot only **writes back** two things: the sentiment it read from the reply, and the "last talked" timestamp. Everything else it just reads.

---

## How the data picks the scenario (routing, in plain words)

The two biggest levers are **Source ("root")** and **Fines**. The simple chains:

- Trademobile + **just bought a car** → **C4 welcome**
- Trademobile + free year + **has fines** → **C2**
- Private / ad + **never subscribed** → **C1 cold**
- Anyone + a **new fine just detected** → **C5** (real-time)
- Anyone + **started an appeal, didn't finish** → **C7** (the coupon one)
- **Lapsed** + has fines → **C3 win-back**
- Anyone + **plan ends within 30 days** → **C6**

On top of that, the bot combines several fields into a simple **"warmth" read** (hot / warm / cold) that decides *how hard to push*: a hot user (paying, has fines, recently active, positive) gets a faster, more direct pitch; a cold or upset user gets a softer touch or nothing at all. If someone is upset **and** high churn-risk **and** silent for months, the bot goes quiet for 30 days — we don't make a bad situation worse.

---

## How the data changes the *message* (not just the scenario)

Same scenario, different person → different words:

- **Source:** a Trademobile person hears *"השירות שקיבלת מטרייד מוביל"* — and **never** the word "leasing" (they bought a car). A private person hears the general pitch.
- **Fines count:** *"איתרנו עבורך 3 דוחות"* — the real number. If it's their 3rd+ fine, we can lean on the double-fine law for extra urgency.
- **Appeal stage:** if the experts are already mid-appeal on a fine, the outbound bot says nothing about that fine — the human team owns it.
- **Gender:** mirrored from their first reply.
- **Honesty about detection:** we only say "we detected your fine" when our radar actually did. For someone who brought their own fine into an appeal, we say "the appeal you started" — claiming we "found" it feels like surveillance.

---

## What we want to achieve

Every message **true and personal**: right name, right gender, right fine count, right partner, no false "we detected," no "leasing." That accuracy is what makes the bot feel like a system that genuinely understands the driver — and that's what converts. A wrong detail (wrong gender, "leasing," a fine count that's off) breaks trust instantly.

---

## How the data flows (simple)

1. The **CRM is the source of truth** — it's where a person's status, fines, and history live.
2. The **bot reads it live** through the API right before each message, so it never acts on stale data.
3. The **bot writes back** two small things: the sentiment of the reply, and when it last talked to the person.
4. A copy of the data also sits in **Smoove**, but that's only for the email newsletter — the bot itself relies on the live API for fines and status.

---

## What we still need (the open gaps)

These came up during the build and are still needed for the bot to be its best:

- **A live "new fine just arrived" trigger** — so C5 can fire the moment a fine lands, exactly like the email already does.
- **A clear plan-tier flag** — today "paying" doesn't tell us Detection vs VIP; several scenarios need to know.
- **A real opt-out flag** — so "remove me" is a clean, reliable signal.
- **An auto-renew flag** — so the "your year is ending" flow doesn't nag people who'll renew automatically.

---

## Out of scope

- B2B partner messaging (Pango, Strauss, etc.) — separate from this bot.
- The exact field names and refresh timings — those live in the technical doc (`../bot-spec/10_crm_integration.md`).
