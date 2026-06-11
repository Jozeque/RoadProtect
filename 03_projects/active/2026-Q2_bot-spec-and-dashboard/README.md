# Bot Spec v2 + Tracking Dashboard

**Status**: 🟡 specing
**Owner**: Yossi
**Started**: 2026-05-26
**Target ship**: 2026-Q3 (spec frozen by end of Q2)
**One-line**: A vendor-ready rewrite of every customer-facing bot flow plus a Hebrew RTL dashboard that tracks the full funnel from message-1 reach to conversion or churn.

---

## Why this exists

Two forces drive this project:

1. **We're switching vendors.** The new vendor needs an unambiguous, complete spec — not a folder of half-finished scenarios. The current scenarios are decent prose but they leak ambiguity (no message-2 cadence, no exit conditions, no event taxonomy, no suppression rules). A new vendor will build to whatever ambiguity we leave them.
2. **We're flying blind on funnel data.** Today we can't answer: "of users we messaged in scenario C5, how many replied to touch 1, how many to touch 2, how many converted, and which of them flagged bad feedback?" Without that we can't tune the bot, we can't price-test the coupon, and we can't justify ramping outbound volume.

Origin: this conversation, 2026-05-26. No prior idea file — this *is* the brief.

## Success metric

**Single metric**: the new vendor builds the bot from this spec without coming back with more than 10 clarification questions before go-live. (Proxy for "the spec is unambiguous.")

Secondary metric, post-launch: within 30 days of dashboard going live, Yossi can answer all six of these unaided —
1. Reach by scenario, last 7 days
2. Reply rate per touch (1/2/3) per scenario
3. Conversion rate per scenario, with attribution to the touch that closed
4. Users who triggered bad-feedback / opt-out signals (with names)
5. Cohort comparison: Trademobile-warm vs cold vs lapsed
6. Top objections by frequency, last 30 days

## In scope

- [x] Rewrite of all 7 C2B scenarios (C1–C7) as multi-touch sequences with explicit timing, exit conditions, branches, events
- [x] Rewrite of B1 inbound flow as intent-router with sub-flows
- [x] Cross-cutting spec: state machine, suppression, frequency caps, opt-out, quiet hours, gender detection, AI disclosure, legal line, escalation
- [x] Dashboard spec: metrics glossary, event schema, funnel model, screen-by-screen UI
- [x] Hebrew RTL HTML mockup of the dashboard
- [x] All bot copy stays in Hebrew (the spec wrapper is English so the vendor can read it; the messages themselves are Hebrew)

## Out of scope

- **English translation of bot copy.** We ship Hebrew. Translation happens *after* this spec is closed 100%, in a separate pass.
- **Actual implementation.** Vendor builds it. We spec it.
- **Email or SMS channels.** WhatsApp only this round — adding channels is a v2 problem.
- **Inbound voice / IVR.** Not a Road Protect surface today.
- **B2B partner-specific flows** (Pango, Strauss, etc.). Those are partner-side messaging, not Road Protect bot. Separate project.
- **New scenarios (C8, B2, etc.).** This round documents and improves the existing 8. New scenarios go through the idea/spec pipeline normally.
- **Dashboard authentication / RBAC.** Assume single internal user (Yossi + team). Auth is a later concern.
- **Real-time alerting on metric anomalies.** Static dashboard first; alerting is v2.

## Status & next action

- **Right now**: spec in draft, structure being built out file-by-file in `bot-spec/` and `dashboard-spec/`
- **Next**: write the cross-cutting framework doc (`bot-spec/00_overview.md`), then rewrite C1 as the reference template, then bash through C2–C7 + B1
- **Blocked on**: nothing — Yossi has approved depth (multi-touch + HTML mockup)

## Documents in this project

- `simple-specs/` — **plain-language, non-technical version of the three specs** (start here for the "what & why"):
  - `1_scenarios.md` — every bot conversation in simple words
  - `2_crm_and_data.md` — what data we have and how it drives each scenario
  - `3_dashboard.md` — what we want to see to run the best bot
- `PRD.md` — overall PRD for the spec rewrite + dashboard project
- `decisions.md` — running log of choices made during the rewrite
- `bot-spec/` — the technical bot spec, one file per scenario + framework + cross-cutting
- `dashboard-spec/` — metrics glossary, event schema, funnel model, screens
- `mockups/dashboard.html` — Hebrew RTL HTML mockup of the dashboard

## Decision log (in-flight)

See `decisions.md`.

---

*When this ships, move to `../shipped/2026-Q2_bot-spec-and-dashboard/` with a retro covering: vendor onboarding questions count, dashboard-first-week usage, what the spec missed.*
