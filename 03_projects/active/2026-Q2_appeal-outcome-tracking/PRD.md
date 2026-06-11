# PRD: Appeal Outcome Tracking — Design Characterization

**Status**: 📝 draft
**Author**: Claude (drafted) / Yossi (approved)
**Last updated**: 2026-05-28
**Version**: 0.1
**Notes**: This doc is more architecture-spec than user-flow PRD because Yossi asked for "אפיון אפילו ברמת רעיונות" — for the developer to pick up.

---

## 1. The problem (concrete)

Today the appeal-submission flow looks like this:

```
RP generates draft → user signs → submitted with USER'S email as contact
                                          ↓
                              Authority responds days/weeks later
                                          ↓
                                 Email lands in user's inbox
                                          ↓
                              [RP has zero visibility]
```

We don't know:
- Whether the appeal was accepted, partially accepted, rejected, or needs more info.
- Which template variants work for which violation types.
- Which municipalities are easier to win against.
- Whether the customer even read the response.

The customer experience also suffers: they get a cold authority email in officialese, no context, no next-step suggestion from RP. The VIP product promise quietly fails because we never close the loop.

## 2. Target user

Two simultaneous users:

1. **The end customer** (P2 — frustrated fresh-fine recipient) — currently gets the authority's email cold and is left alone with it. The pipe we build serves them by delivering a parsed, friendly, actionable response inside RP's channels.
2. **Road Protect itself** — needs per-fine outcome data to measure, learn, and improve. This is the higher-priority user for v1.

## 3. The hypothesis

We believe that **routing all appeal responses through an RP-controlled inbound channel** will cause **automated capture, attribution, customer notification, and acceptance-rate measurement** for **every camera-fine appeal we submit**.

We'll know we're right if **≥80% of post-launch appeals have an outcome record auto-attributed and parsed** within **the response window (typically 60–120 days from submission)**.

## 4. Success metric (the one number)

**Auto-attribution rate**: the percentage of submitted appeals where, when an authority response arrives, it is correctly attributed to the right `fine_id` and parsed into a structured outcome — without manual intervention.

- Baseline: 0%
- Target v1: ≥80%
- Stretch: ≥95% within 90 days post-launch

This is a *plumbing* metric, not a product metric. The product metric — acceptance rate — is enabled by this, not measured here.

## 5. Three architectural options (and the pick)

The fundamental design question: **how does the response get to RP?**

### Option A — RP-owned alias per fine ⭐ **picked**

```
RP generates draft with contact email: appeal-{fine_id}@appeals.roadprotect.co.il
                ↓
       Authority responds to that alias
                ↓
   RP inbound parser tags response by fine_id → outcome record
                ↓
       Customer notified in-app + WhatsApp
```

**Pros**:
- 100% clean attribution (`fine_id` is in the address itself).
- Single source of truth in our DB.
- Customer gets a strictly better experience (parsed, branded, in-app).
- Foundation for future automation.

**Cons**:
- Requires the appeal form to accept a contact email different from the signatory's personal email. **Must verify with legal/compliance.**
- Some authorities might cross-reference contact email vs. registered owner. Low likelihood but real.
- Need inbound email infra (subdomain, MX records, inbound parser service).

### Option B — OAuth mail-forwarding from customer's inbox

```
User signs into RP and authorizes Gmail/Outlook OAuth scope
                ↓
RP installs a forwarding rule: if subject/body contains fine_id → forward to RP
                ↓
       Customer's inbox + RP's inbox both receive
```

**Pros**: Customer-owned email stays primary on the appeal — no legal ambiguity.

**Cons**:
- ~85% coverage at best — anyone on ISP email / custom domain isn't covered.
- OAuth scope `mail.read` is sensitive. Many users will refuse during onboarding.
- Per-provider implementation (Gmail API + Microsoft Graph API + maybe more).
- Brittle — users revoke OAuth, change passwords, switch providers.

### Option C — Manual upload prompt

```
30 days post-submission, RP sends WhatsApp: "Did you get a response? Forward it"
                ↓
        Customer forwards / uploads the email
                ↓
                 RP parses
```

**Pros**: Zero infra. Ships in a sprint.

**Cons**: ~30-50% response rate at best. Customer fatigue. The customers who *don't* respond are often exactly the ones whose appeals were rejected (silence correlates with bad news). Biased data.

### Pick: A as primary, C as fallback. B deferred to Phase 2.

A + C together gives us:
- Automatic capture for the canonical path
- A human safety net for cases where the authority responds by physical mail, or by email to a different address, or anything we miss

OAuth (B) is real complexity for marginal coverage. Revisit only if A turns out to be legally blocked.

## 6. Architecture — Option A in detail

### Data flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. APPEAL SUBMISSION                                               │
│     - RP generates appeal draft for fine_id=F123                    │
│     - Alias generated: appeal-F123@appeals.roadprotect.co.il        │
│     - Appeal form: contact_email = the alias                        │
│       (user's personal email kept in the appeal text body)          │
│     - User signs, RP sends                                          │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                      [days / weeks pass]
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  2. INBOUND CAPTURE                                                 │
│     - Authority email arrives at appeal-F123@appeals.roadprotect... │
│     - Provider routes via MX → inbound parser webhook               │
│       (SendGrid Inbound Parse / Postmark / AWS SES — make-or-buy)   │
│     - fine_id extracted from local-part of the address              │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  3. PARSE                                                           │
│     - First pass: regex/heuristics on common Hebrew phrases         │
│       e.g. "התקבל / נדחה / בוטל / הופחת לסך ... / חסר מסמך ..."     │
│     - Confidence > 0.85 → write to outcomes table                   │
│     - Confidence ≤ 0.85 → LLM classifier (gemini/claude haiku)      │
│     - Still unsure → human review queue                             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  4. PERSIST                                                         │
│     - outcomes table updated (schema in §7)                         │
│     - fine record gets status: pending → resolved                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  5. CUSTOMER NOTIFICATION                                           │
│     - WhatsApp via bot pipeline (uses existing channel)             │
│     - Email summary from RP (NOT the raw authority email)           │
│     - In-app status badge updates                                   │
│     - If positive outcome: ask for review/testimonial               │
│     - If negative: offer next-step (appeal escalation, etc.)        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│  6. METRICS                                                         │
│     - Acceptance-rate dashboard updates                             │
│     - Per-camera-type, per-municipality, per-template breakdowns    │
│       (feeds Camera-Type Detection success metric)                  │
└─────────────────────────────────────────────────────────────────────┘
```

### The fallback path (Option C, runs in parallel)

```
60 days post-submission, fine has no outcome record →
   Send WhatsApp: "האם קיבלת תשובה לערעור? אם כן, העבר אלינו או צלם".
   Customer responds via the bot, gets parsed by the same parse stage,
   tagged "source: manual_capture".
```

## 7. Database schema (idea-level, not final)

```sql
-- New table
outcomes (
  id                    uuid PK
  fine_id               uuid FK → fines.id
  status                enum('cancelled', 'reduced', 'rejected',
                             'request_info', 'partially_accepted',
                             'unknown')
  amount_before         numeric        -- ₪
  amount_after          numeric        -- ₪
  points_before         int
  points_after          int
  response_raw          text           -- the original email body
  response_subject      text
  response_from         text           -- the authority's email
  response_received_at  timestamptz
  source                enum('email_alias', 'manual_upload',
                            'oauth_forward')
  parse_confidence      float          -- 0.0 to 1.0
  parsed_by             enum('regex', 'llm', 'human')
  parsed_at             timestamptz
  reviewer_notes        text           -- if a human reviewed
);

-- New index for the parser webhook
CREATE INDEX idx_outcomes_fine_id ON outcomes(fine_id);

-- Update to fines
ALTER TABLE fines
  ADD COLUMN appeal_alias_email text UNIQUE,
  ADD COLUMN appeal_submitted_at timestamptz,
  ADD COLUMN appeal_outcome_status enum(...) DEFAULT 'pending';
```

### The alias format

`appeal-{fine_id_b32}@appeals.roadprotect.co.il`

Use base32 (not raw UUID) for shorter, copyable addresses. ~13 chars. Verify the authority's appeal form accepts this length.

## 8. Requirements

### Must have (v1 ships without these = no go)
- [ ] **R1** Subdomain `appeals.roadprotect.co.il` with MX records pointing to inbound-mail provider.
- [ ] **R2** Inbound-mail provider integrated (recommend: AWS SES inbound + S3 + Lambda, or SendGrid Inbound Parse — make-or-buy decision is a SPEC concern).
- [ ] **R3** Alias-per-fine generation at appeal submission time.
- [ ] **R4** Appeal-submission flow updated to use alias as contact. ⚠️ **Legal check first.**
- [ ] **R5** Inbound parser: regex pass + LLM fallback + human queue.
- [ ] **R6** `outcomes` table and `fines` table changes per §7.
- [ ] **R7** Customer notification on outcome — WhatsApp + email + in-app. Reuse existing bot pipeline.
- [ ] **R8** Manual-upload fallback path with "60-day no-response" trigger.
- [ ] **R9** Ops dashboard: parse rate, confidence distribution, unparsed queue, time-to-parse.

### Should have (v1.1 or fast-follow)
- [ ] **R10** Per-municipality outcome breakdown (informs which municipalities accept appeals at what rate).
- [ ] **R11** Per-template outcome breakdown (closes the loop for Camera-Type Detection).
- [ ] **R12** Auto-escalation logic when an authority response says "missing document" — kick off a sub-flow to gather and resubmit.
- [ ] **R13** Outcome-export API for fleet/B2B clients (Trademobile, Tir, etc.).

### Won't have (this round)
- **R14** OAuth-based mail forwarding (Phase 2).
- **R15** Physical-mail OCR (out of scope; we'll never see paper mail).
- **R16** Predicting outcome before submission (different ML project).

## 9. Edge cases & error states

- **Authority responds from a different address than expected** — capture works regardless; we route on the *to* address, not the *from*.
- **Authority CC's customer's personal email** — fine; customer gets two copies, ours wins in-app.
- **Customer changes email** — alias is fine-bound, not customer-bound. Not an issue.
- **Authority responds to the appeal text body's mention of customer's email instead of the contact field** — likely 5–10% of cases. Manual-upload fallback catches these.
- **Same fine, multiple appeals** — each appeal gets its own alias. Multiple `outcomes` rows per fine, ordered by `response_received_at`.
- **Authority sends "thank you, we received" auto-acks** — parser must classify as `acknowledgement` (not yet an outcome). Add to enum.
- **Spam to the appeals subdomain** — SPF/DKIM/DMARC + sender-domain allowlist of known authorities (gov.il, municipal domains).
- **Parser confidence too low across the board** — falls into human queue; if queue grows beyond N items/day, alert ops.

## 10. Legal / compliance review

This is the **blocker** to validate before development starts.

1. **Can the appeal contact email be different from the signatory's personal email?**
   The user is the legal author of the appeal. The contact email is administrative. There's no Israeli regulation I'm aware of requiring the contact email to match a personal identifier. **But — verify.** Worth a 30-minute call with RP's legal contact before we commit engineering hours.

2. **Customer consent to receive parsed authority correspondence via RP.** Add to VIP onboarding T&C: "Road Protect will receive on your behalf the responses to appeals it generates, parse them, and notify you. Original copies are available on request."

3. **Data retention.** Authority responses are personal data. Retention policy: keep raw response for X years (verify with privacy), purge or anonymize beyond.

4. **The legal disclaimer in `01_business_context/LEGAL_DISCLAIMER.md` is unaffected.** We're not adding legal representation — we're administrating correspondence. Word the T&C carefully to preserve this.

## 11. Rollout plan

**Stage 0 — Pre-build legal validation (1 week)**
- Verify Q1 (alias-as-contact-email) is allowed. Hard gate.

**Stage 1 — Internal pilot (weeks 1–3)**
- Build the alias + inbound + parser pipeline.
- Use on 100% of new appeals from internal RP test accounts.
- Validate end-to-end with synthetic authority responses + real ones.

**Stage 2 — 10% rollout (week 4)**
- Real customer appeals, 10% of incoming.
- Track parse rate, confidence distribution, manual-queue size.
- Gate to next stage: parse rate ≥80%, no unresolved support tickets attributable to the new flow.

**Stage 3 — 50% (week 5)**

**Stage 4 — 100% (week 6)**

**Rollback**: per-fine feature flag. Reverting means future appeals use the old "user's email as contact" path. Already-submitted appeals continue listening on their aliases regardless of flag state.

## 12. Open questions

- **Q1** ⚠️ **Hard blocker**: Can the appeal contact email be RP-controlled? Legal check.
- **Q2**: Make-or-buy on inbound parsing? AWS SES Inbound + Lambda vs. SendGrid/Postmark managed parse. Cost difference probably <₪500/month at our scale.
- **Q3**: Do we already have a Hebrew NLU/LLM in use elsewhere in RP we can reuse for the parser fallback, or is this a new dependency?
- **Q4**: Which authorities are highest-volume responders? We should prioritize parser tuning on those (likely police + Tel Aviv + Jerusalem + a few more).
- **Q5**: When the outcome is `request_info`, what's the auto-flow? Notify customer + open a task for the appeal-handling team? Defining this affects v1 scope.
- **Q6**: How long does an authority typically take to respond? If 90+ days is normal, our 60-day fallback trigger should be 90.

## 13. Out of scope (reiterating)

- OAuth mail-forwarding from customer accounts (Phase 2).
- Predicting outcomes before submission.
- Paper-mail OCR.
- Fleet/B2B outcome export (fast-follow, R13).
- Visualizing acceptance-rate trends for end users.
- Outbound auto-escalation when rejected (different project).

---

*This doc is the developer's brief. Tech spec lives in `SPEC.md` once direction is approved.*
