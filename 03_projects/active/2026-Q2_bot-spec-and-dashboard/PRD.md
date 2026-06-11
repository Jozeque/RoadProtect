# PRD: Bot Spec v2 + Tracking Dashboard

**Status**: 📝 draft
**Author**: Claude (drafted) / Yossi (approving)
**Last updated**: 2026-05-26
**Version**: 0.1

---

## 1. Problem

Two concrete problems.

**Problem A — vendor-handoff ambiguity.** Road Protect is switching the bot vendor. The current scenarios in `06_bot/scenarios/` describe an opening message and reply branches, but they don't specify: when the second touch fires, when the sequence exits, what events are emitted, what happens when a user is eligible for two scenarios at once, what the daily / lifetime frequency cap is, what quiet hours apply, or what a "bad feedback" signal even is. A new vendor will build to the gaps, and the gaps are the parts that determine whether the bot is good or annoying.

**Problem B — funnel blindness.** Today, "how many users we reached, how many replied to touch 1, touch 2, how many converted, and who had bad feedback" cannot be answered without manual log spelunking. There is no dashboard. There is no event schema that would *support* a dashboard. Decisions about coupons, cadence, and audience expansion are being made on vibes.

Both problems compound: without the dashboard, we can't tell whether the rewritten scenarios are better than the originals. Without the rewritten scenarios, the dashboard's funnel structure is undefined.

## 2. Target user

**Two users, both internal.**

- **The new bot vendor's product/engineering team** — reads the spec to build. Needs unambiguous trigger predicates, message text in Hebrew, exit conditions, event names, suppression rules. Cannot ask Yossi during build.
- **Yossi (and any growth/ops person added later)** — uses the dashboard to tune the bot weekly. Needs: funnel by scenario, drill-down to individual users, bad-feedback flagging, cohort comparison.

(No external user persona in this PRD — the end-user impact is mediated through the bot, which is specified separately per scenario.)

## 3. The hypothesis

We believe that **shipping a complete, multi-touch, event-instrumented spec + a Hebrew RTL dashboard** will cause **a measurable lift in conversion per scenario and a sharp drop in vendor-handoff friction** for **the Road Protect bot stack**.

We'll know we're right if **(a) vendor onboarding requires fewer than 10 clarification questions before go-live, and (b) within 60 days of dashboard launch we identify at least one scenario whose touch-2 reply rate is materially below touch-1, triggering a copy or timing rewrite that improves it**.

## 4. Success metric (the one number)

**Primary metric**: Number of vendor clarification questions between spec handoff and go-live. **Target: ≤ 10.** Baseline: undefined (no prior handoff) — but we know that the current scenarios alone would generate dozens (no timing, no exits, no events).

How measured: count Slack/email/ticket questions from the vendor referencing the spec, between spec freeze date and bot-live date. Yossi maintains the count manually during onboarding.

## 5. Secondary metrics & guardrails

**Secondary:**
- Time from spec freeze → vendor go-live (target: ≤ 4 weeks)
- Within 30 days of dashboard launch: Yossi can answer the 6 questions listed in `README.md` § Success metric unaided.
- Reply rate at touch-2 across all C2B scenarios (baseline TBD, but we want this visible — it's the metric we don't currently have)

**Guardrails:**
- **Opt-out rate must stay ≤ 2% per scenario per month.** If a rewritten scenario crosses that, the touch cadence is wrong — pull it back.
- **Bad-feedback signal rate must stay ≤ 1% per scenario per month.** If higher, the copy is off.
- **Complaint-to-message ratio across all C2B output must stay ≤ 0.5%.** If higher, slow the volume globally.

## 6. User journey / flow

Two parallel journeys.

### 6.1 Vendor journey

1. Vendor receives `bot-spec/` + `dashboard-spec/` + mockup.
2. Vendor reads `bot-spec/00_overview.md` first (the framework).
3. Vendor reads each scenario file. Each scenario is self-contained — trigger, touches, branches, events, exits.
4. Vendor reads `bot-spec/09_cross_cutting.md` for rules that apply to every scenario.
5. Vendor builds. Hopefully <10 questions back.

### 6.2 Yossi journey (dashboard)

1. Opens dashboard. Lands on **Funnel Overview** — 7 C2B scenarios as a vertical list, each showing: reached → touch-1 replied → touch-2 replied → touch-3 replied → converted → opted-out. Last 7 days, last 30, last 90 toggle.
2. Clicks a scenario → **Scenario Drill-down**: touch-level conversion, reply-content samples, bad-feedback users (with names + phone), top objections.
3. Clicks **Users panel** → who replied to which touch, who's mid-sequence, who opted out, who flagged bad feedback. Searchable / exportable.
4. Clicks **Cohorts** → side-by-side comparison of Trademobile-warm vs cold vs lapsed funnel.

Mockup of all four screens lives in `mockups/dashboard.html`.

## 7. Requirements

### Must have (v1 ships without these = no go)

**Bot spec side:**
- [ ] R1: Every scenario file has explicit trigger predicate (machine-readable, not prose)
- [ ] R2: Every C2B scenario specifies touch 1, touch 2 (with delay), touch 3 (with delay), or explicitly states "single-touch only" with reason
- [ ] R3: Every scenario specifies exit conditions (replied / converted / opted-out / suppressed / timer expired)
- [ ] R4: Every scenario specifies events emitted per touch (the canonical event names from `dashboard-spec/02_event_schema.md`)
- [ ] R5: Cross-cutting doc specifies: frequency caps, suppression matrix, opt-out trigger phrases, quiet hours, Shabbat handling, gender detection rule, AI disclosure rule, legal-line rule, escalation triggers
- [ ] R6: B1 inbound has intent taxonomy with explicit classification rules and per-intent sub-flows
- [ ] R7: All Hebrew copy is RTL-correct and matches the brand voice in `06_bot/knowledge_base/voice_and_tone.md`

**Dashboard side:**
- [ ] R8: Event schema covers: reach, deliver, read, reply, convert, opt-out, bad-feedback, escalation, sequence-exit
- [ ] R9: Funnel model defined per scenario (which events count toward which funnel step)
- [ ] R10: Screen spec covers: overview, scenario drilldown, users panel, cohorts panel
- [ ] R11: Hebrew RTL HTML mockup of all four screens
- [ ] R12: Bad-feedback definition is precise — what phrases / signals trigger the flag, not "user seemed unhappy"

### Should have (v1.1 or fast-follow)

- [ ] R13: A/B variant slots defined per touch (so the vendor can instrument A/B from day one)
- [ ] R14: Per-touch quality checklist (length, gender, legal line) inline in each scenario file
- [ ] R15: Mockup shows realistic numbers (not zeros) so Yossi can react to the layout

### Won't have (this round)

- R16: Real-time alerting on metric anomalies — deferred
- R17: Drill-down all the way to individual message-level event logs — only down to user-level
- R18: Translation of bot copy to English — happens after spec is frozen 100%
- R19: B2C inbound expansion beyond intent routing (e.g. deep multi-turn diagnosis flows) — current B1 scope only

## 8. Edge cases & error states

- **User eligible for two scenarios at once** (e.g. lapsed + has new fine = C3 *and* C5). Suppression matrix in `09_cross_cutting.md` says which wins.
- **User opts out mid-sequence.** All future touches in all scenarios canceled. Logged. Dashboard shows the user in the opt-out list.
- **Quiet hours hit mid-sequence.** Touch deferred to next eligible window. Not sent late at night.
- **WhatsApp delivery fails** (number invalid, blocked). Mark as undeliverable. Stop the sequence. Don't retry.
- **User replies to a touch already exited from** (e.g. sequence ended, they reply 2 weeks later). Bot handles via B1 inbound flow, not by resuming the old sequence.
- **User sends abusive / legal-threat content.** Escalate per `09_cross_cutting.md` escalation rules. Pull from sequence.
- **Variable substitution fails** (e.g. `{{name}}` empty). Either skip the touch or use a fallback opener. Specified per scenario.
- **Coupon already redeemed** when C7 fires. Suppress C7 for that user.

## 9. Legal / compliance review

- Every scenario must comply with `01_business_context/LEGAL_DISCLAIMER.md`. No "lawyers represent you", no guaranteed cancellation, no "we submit on your behalf".
- AI disclosure: when user asks who they're talking to, bot must respond "אני סוכן AI דיגיטלי / העוזר הדיגיטלי של Road Protect". This is checked at every scenario.
- Opt-out mechanism must be honored within one message cycle.
- Quiet hours respect Israeli norms: 22:00–08:00 weekday, all of Shabbat (Friday 17:00 → Saturday 21:00 local).
- Data retention for dashboard: user identifiers stored only as long as the user is active or 24 months post-churn, whichever is longer. Anonymize beyond that.
- Israeli Privacy Protection Law (חוק הגנת הפרטיות) — outbound WhatsApp to existing customers / leads is permissible based on consent given at signup. Cold-list outreach (C1) requires existing-relationship grounding (the "השארת אצלנו פרטים בעבר" framing).

## 10. Rollout plan

- **Internal review** — Yossi reviews each spec file as it lands. Comments → revisions.
- **Spec freeze** — once all files are signed off, mark `bot-spec/` and `dashboard-spec/` as v1.0.
- **Vendor handoff** — ship the spec folders + mockup to the new vendor.
- **Vendor builds bot** — track clarification questions toward the success metric.
- **Bot goes live in shadow mode** — bot runs but only on 5% of eligible users per scenario, dashboard tracks the events, Yossi compares funnels to legacy bot.
- **Graduate to full traffic** when: each scenario's touch-1 reply rate ≥ legacy baseline AND opt-out rate ≤ 2%. Per-scenario, not all at once.
- **Rollback plan**: shadow-mode users are a controlled cohort — if any scenario crosses guardrails, route those users back to the legacy bot or pause outbound entirely while we diagnose.

## 11. Open questions

- **What's the actual delivery channel API?** WhatsApp Business Cloud API, 360dialog, Twilio? This affects event-emission granularity (read receipts available or not). → Need answer from Yossi / vendor.
- **Is there a CRM of record** the bot reads from / writes to? Or is the bot stateful itself? → Affects "where does suppression state live" in the spec.
- **Coupon** — resolved (Yossi, chat 28/04–30/04): one code, `SAVE30` = 30% off the one-off appeal (₪49), in C7 only. No ladder, no 50%, no coupon on VIP. C3/C6 issue no coupon. (See decisions log, 2026-06-03.)
- **"Bad feedback" definition** — currently I'm defining as: explicit complaint phrase, refund/cancel request, "stop messaging me", escalation to legal-threat. Yossi to confirm this list is complete.
- **Trademobile data feed** — what's the freshness? Affects whether C4 welcome fires within 24h is realistic.
- **Real baseline numbers** for current scenarios — needed to validate the dashboard's mockup numbers are realistic (not blockers for the spec, but for the rollout).

## 12. Out of scope (saying it again because it always matters)

- No English translation of bot copy this round.
- No new scenarios — only documenting and improving the 8 existing.
- No actual implementation by Claude — vendor builds.
- No B2B partner messaging.
- No SMS / email channel expansion.
- No dashboard auth/RBAC.

---

*PRD owned by Yossi. Once approved, marked 🔒 frozen and handed to the vendor with the rest of `bot-spec/` and `dashboard-spec/`.*
