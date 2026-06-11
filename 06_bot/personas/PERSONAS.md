# User Personas

Who the bot is actually talking to. These are working approximations — refine when real user research is in.

---

## P1 — The Trademobile new-car buyer

**Who:** Bought a used car in the last 30 days via Trademobile. Got the free Detection year as a bundled perk. May not even remember signing up.

**Mindset:**
- Excited about the new car
- Vaguely aware that "some service" was attached but hasn't engaged
- Not actively thinking about fines (yet)

**Pain points:**
- Hasn't experienced a fine in this car yet
- The 50% interest / double-fine info is news to them
- Doesn't know what Road Protect is until the welcome message

**How the bot should engage:**
- Variant A welcome (informative, value-first)
- Don't pitch VIP in the first message — establish what the free year is doing
- Set up for the "first fine detected" moment to be a clean win

**Conversion path:**
Welcome → fine detected (at some point in year) → VIP pitch on that moment → pre-expiry retention

---

## P2 — The frustrated fresh-fine recipient

**Who:** Got a fine notification (from us or from the post). Is currently annoyed. Often midway through their day.

**Mindset:**
- Angry / frustrated / "this is ridiculous"
- Wants the problem to go away
- Suspicious of upsell at this moment

**Pain points:**
- Doesn't want to lose more time on the fine
- Doesn't want to pay more than they have to
- Skeptical that "appeal" is a real option vs. just paying

**How the bot should engage:**
- Empathy first ("איזה באסה")
- Then the appeal angle — "המון דוחות מתבטלים..."
- Don't pile on urgency on top of their existing frustration; replace their frustration with hope

**Conversion path:**
Empathy → appeal explanation → VIP or one-off pitch → close

---

## P3 — The skeptic (cold lead)

**Who:** Left details on the site months ago. Never converted. Probably forgot about Road Protect.

**Mindset:**
- "Who is this messaging me?"
- "What's the catch?"
- Possibly mildly annoyed at being contacted

**Pain points:**
- Has no immediate need they're aware of
- Doesn't trust unsolicited contact
- Won't engage with a hard sell

**How the bot should engage:**
- Reminder of past contact ("השארת אצלנו פרטים בעבר")
- Lead with the *problem* (fines that disappear in the mail), not the solution
- Soft question — "do you have a fine?" — not a pitch

**Conversion path:**
Cold → reply → diagnostic → one-off (most likely) or Detection

---

## P4 — The about-to-lapse Trademobile cohort

**Who:** 30 days from the free Detection year ending. Has been a passive user. May or may not have had fines detected during the year.

**Mindset:**
- "What's actually been happening here?" (Probably hasn't checked their account)
- Price-sensitive — was free, now isn't
- Possibly thinking "I don't need this, nothing happened"

**Pain points:**
- Can't articulate the value because nothing went wrong (or because the value was the absence of pain)
- Time pressure — they need to decide before expiry

**How the bot should engage:**
- Lead with what we did for them (X scans, Y fines detected, even if "nothing detected" is the result — frame that as "we made sure nothing went wrong")
- FOMO about losing protection
- Show VIP as the upgrade, not Detection as the continue

**Conversion path:**
30-day reminder → 14-day → 3-day → day-of with possible coupon (escalates to C7)

---

## P5 — The lapsed user with a fresh fine

**Who:** Was a subscriber, lapsed, and now has detected a new fine on a check.

**Mindset:**
- Has historical relationship — knows the product
- Lapsed for a reason (price, didn't see value, churn event)
- Now sees a concrete cost of not being subscribed

**Pain points:**
- "If I'd had VIP, this would be handled already"
- Coupon-receptive

**How the bot should engage:**
- Acknowledge the lapse without guilt-tripping
- Concrete: "you have a fine right now; here's what VIP would do"
- Coupon is appropriate here (30%, occasionally 50%)

**Conversion path:**
Detection of fine → acknowledgment → VIP pitch w/ coupon → close

---

## P6 — The B2C inbound

**Who:** Found the WhatsApp number, started a conversation themselves.

**Mindset:**
- Has an actual question or problem — they wouldn't have messaged otherwise
- Either: got a fine and looking for help, OR researching the product
- Reasonably engaged from message one

**Pain points:** depend on the sub-intent (handled in `b2c/01_inbound_entry.md`)

**How the bot should engage:**
- Friendly opener
- Quick diagnostic question to route
- Once routed, follow the right sub-flow

---

## Cross-persona principles

- **Trademobile cohort (P1, P4) gets the "we're already protecting you" framing.** They've been onboarded.
- **Fresh-fine recipients (P2, P5) get empathy + appeal framing.** Don't sell to angry people; solve.
- **Cold and inbound (P3, P6) get diagnostic questions.** Don't pitch before knowing.
