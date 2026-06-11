# Road Protect — Company Brief

*This is the single source of truth for Road Protect facts. Update it when reality changes. Everything else (specs, mockups, copy, bot scenarios) is downstream of this file.*

---

## One-line pitch

Road Protect is an Israeli driver's active radar for traffic and parking fines: it detects fines across police + 20+ municipal databases the moment they're registered, alerts via WhatsApp/email, and (on VIP) handles the appeal end-to-end.

## The problem (why this exists)

Israeli drivers lose money to fines they never knew about. The mechanics:

1. Fine is issued (camera, parking, etc.) and registered in the municipal/police system.
2. A paper letter is mailed — and frequently lost, delayed, or sent to an old address.
3. The driver misses the payment window. The fine **automatically jumps 50%** in late-payment interest.
4. After 4 unhandled fines in 3 years, fines start **doubling**.
5. License points accumulate silently. Driver finds out at license renewal or when pulled over.

The product attacks step 2 (alert before the letter ever arrives) and step 5 (appeal to cancel before points stick).

## The product, layered

### Layer 1 — Detection (radar)
- 24/7 scanning of: Israel Police + ~22 municipality databases (Tel Aviv, Jerusalem, Haifa, Rishon LeZion, Petah Tikva, Ashdod, Netanya, Be'er Sheva, Holon, Bnei Brak, Ramat Gan, Ashkelon, Rehovot, Bat Yam, Herzliya, Kfar Saba, Hadera, Modi'in, Nazareth, Lod, Ra'anana, and others).
- WhatsApp + email alert the moment a fine is detected under the user's name or plate.
- Sold standalone at ₪99/year ("Detection" plan) or bundled into VIP.

### Layer 2 — Appeal pipeline
- User uploads the fine (or it's auto-attached from Layer 1).
- System generates an appeal draft tailored to the violation type and the regulating authority.
- User reviews, edits, signs, and submits. **Critical legal point**: Road Protect generates the draft; the user submits. We are not a law firm.

### Layer 3 — VIP (the upsell)
- Everything in Detection + unlimited appeals per year, late-fee absorption (company pays the 50% interest if it accumulates during our handling), municipal payment integration, lawyer referral for edge cases.
- ₪489/year.
- This is the margin product. Detection is the funnel.

### One-off
- ₪49 per single appeal, no subscription. Tactical product for people who got one fine and don't want to commit.

## Pricing snapshot (current — May 2026)

| Plan | Price | Frequency | Notes |
|---|---|---|---|
| Detection | ₪99 | annual | ₪8.25/mo equiv. Funnel product. |
| **VIP** | ₪489 | annual | ₪40.75/mo equiv. 31% "saving" vs monthly framing. **Recommended tier.** |
| One-off appeal | ₪49 | one-time | No expiry. |

## Distribution channels

### B2C direct
- Website signup → onboarding → free trial mechanics TBD (verify with Yossi).
- WhatsApp inbound (the C2B agent handles this).
- Organic SEO on fine-related queries (the `/magazine` content hub).

### B2B partnerships
- **Pango** — parking-payments app. Cross-promo.
- **Trademobile** — used-car platform. **Key channel**: every car purchase comes with 1 free year of Detection. This is the warm-list source for the C2B agent.
- **Touch, Strauss, Samelet, Tir, Leasecom, Akiva** — corporate / fleet clients.
- **Ashkelon municipality** — interesting reverse partnership (the city is also a customer).

### Backers
- Badger Holdings.
- Getdismissed (US) — adjacent player in US ticket-dismissal market. Strategic + likely playbook source.

## The 2026 traffic reform context

The reform shifted Israeli traffic-fine handling from a potential criminal-court route to an **administrative, document-based process**. Implications:

1. Drivers can no longer "have their day in court" — appeals are paper/digital only.
2. **The quality of the written appeal matters more**, because the document is the entire case.
3. Road Protect's automated, structured drafting is **more valuable post-reform**, not less. Lead with this in 2026 messaging.
4. Awareness is still low. There's a window to be the brand that "explains the reform" — see the magazine strategy.

## Key numbers (claimed on site; treat as marketing until verified)

- 30,000 drivers protected.
- 10M+ fines issued in Israel per year (≈ 1 every 3 seconds).
- 29% YoY increase in traffic-case enforcement (2024→2025).
- ₪2,150 average fine spend per driver over 3 years.
- 50% late-payment interest, automatic doubling from the 4th unhandled fine in 3 years.

**TODO for Yossi**: provide internal numbers — active subscribers, MRR, churn, ARPU, conversion from Detection→VIP, conversion from Trademobile-free-year→paid. Put them in `09_metrics/KPIs.md` when ready.

## The legal line (memorize)

> Road Protect provides a digital environment and technological tools for self-management and self-drafting of traffic-fine appeal documents. **The service does not constitute legal advice, is not provided by a law firm, and does not include representation before authorities on your behalf.** The system creates a draft based on the information and selections you provide; **you are solely responsible** for reviewing the draft, editing it, verifying factual accuracy, and submitting per applicable rules.

This phrasing is non-negotiable. All bot scenarios, marketing copy, and product UI must be consistent with it.

## Open strategic questions (the PM agenda)

These are the live questions to push thinking on. Each should eventually become a project or be answered.

1. **Detection→VIP conversion** — what's the rate, and what's the highest-leverage lever (in-product trigger, timed email, WhatsApp nudge, price test)?
2. **Trademobile free-year cohort** — what % renews paid? How does the existing winback flow perform? Is the coupon (30% / 50%) the right lever or is it price anchoring?
3. **Per-municipality appeal success rates** — do we have data on which cities accept appeals at what rate? If yes, we can productize "highest-cancellation-likelihood" routing. If no, this is a data-collection project.
4. **B2B fleet product** — is there a productized fleet dashboard or is each partner bespoke? If bespoke, what's the right v1 self-serve fleet plan?
5. **Pricing test** — VIP at ₪489 vs a monthly ₪59 option. Annual locks LTV but suppresses top-of-funnel. Worth testing.
6. **The "appeal verification" surface** (`/fine-verification`) — what is this doing today and is it a discovery wedge for people who don't know they have a fine?

---

*Last updated: 2026-05-26.*
