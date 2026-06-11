# Bot Scenarios — Index

Road Protect runs two WhatsApp agents:

- **C2B agent** — *outbound*. Initiates conversations with prospects and existing users at specific lifecycle moments.
- **B2C agent** — *inbound*. Responds to users who message Road Protect WhatsApp themselves, and to users reacting after an alert.

Both agents are AI-powered (the agent identifies itself as "a digital AI agent of Road Protect"). They share a knowledge base (`../knowledge_base/`) and a set of personas (`../personas/`).

## All scenarios

### C2B (outbound)

| # | Trigger | Audience | File |
|---|---|---|---|
| C1 | Cold reach to leads who left details previously | "Cold" (never subscribed) | `c2b/01_cold_outreach.md` |
| C2 | Re-engagement of Trademobile free-year users who have detected fines | Trademobile cohort with ≥1 fine | `c2b/02_trademobile_active.md` |
| C3 | Win-back of churned past customers with detected fines | Lapsed users with ≥1 fine | `c2b/03_past_customer_winback.md` |
| C4 | Welcome new Trademobile car buyer | New Trademobile customer | `c2b/04_trademobile_welcome.md` |
| C5 | Free-tier user just got a fine — push to VIP | Detection user with new fine | `c2b/05_free_user_got_fine.md` |
| C6 | 30 days before free-year expiry — retention | Detection users approaching expiry | `c2b/06_pre_expiry_retention.md` |
| C7 | "Dirty & Quick" — finish the abandoned appeal with 30% off (SAVE30) | Users who started a single appeal and dropped before payment | `c2b/07_dirty_and_quick_winback.md` |

### B2C (inbound)

| # | Trigger | File |
|---|---|---|
| B1 | User initiates WhatsApp conversation | `b2c/01_inbound_entry.md` |

## Cross-cutting

- `../personas/` — who is the bot talking to and what do we know about them
- `../knowledge_base/objection_library.md` — common pushbacks and the answers
- `../knowledge_base/faq.md` — factual questions users ask
- `../knowledge_base/escalation_rules.md` — when the bot hands off to a human
- `../knowledge_base/voice_and_tone.md` — how the bot sounds

## Principles (extracted from the existing scripts)

1. **Question-back, never monologue.** Every message ends in a question to keep the conversation moving.
2. **Gender-neutral until detected.** Use "ברצונך / שלך / עבורך" until the user's reply reveals masculine/feminine, then switch. The bot is supposed to detect from the first response.
3. **One clear CTA per message.** Either a link to the landing page or a "כתוב לי 'אשמח לפרטים'" trigger.
4. **Empathy first, urgency second, sale third.** Especially when responding to a user who just got a fine — acknowledge the frustration before pivoting.
5. **The legal line is the legal line.** Never imply lawyer representation. "Experts" / "team" / "drafts the appeal in your name" — yes. "Lawyers will represent you" — no. And never promise cancellation — we "fight to maximize the chances of cancellation," handle the bureaucracy, and minimize damage.
6. **Identify as AI when asked.** "אני סוכן AI דיגיטלי" / "אני העוזר הדיגיטלי של Road Protect."
7. **Identify the brand up front.** Users mistake a fine alert for the municipality — open outbound messages with "כאן צוות Road Protect."
8. **Coupon = 30% on the single appeal, abandoners only.** Code is `SAVE30`. No 50%, no "choose your discount," never a coupon on VIP. Cold / no-fine cohorts get no coupon. Convert gradually: close the cheap appeal first, upsell VIP later.
9. **Appeals route to the appeals department — don't re-collect fine details.** When a user wants to appeal, hand them to the appeals WhatsApp (052-586-6982) with a "send 'היי'" CTA. Don't make them re-type details the appeal flow will ask for.
10. **Trademobile = car purchase, never leasing.** For Trademobile cohorts, reference "טרייד מוביל" by name and frame the free year as "השירות שקיבלת מטרייד מוביל." Never say "חברת ליסינג."
