# Appeal Outcome Tracking

**Status**: 🟡 specing
**Owner**: Yossi
**Started**: 2026-05-28
**Target ship**: 2026-Q3 (4–6 weeks from kickoff, before Camera-Type Detection ships)
**One-line**: Capture every authority response to an appeal automatically, file it per-fine, notify the customer, and feed the acceptance-rate dashboard.

---

## Why this exists

Triggered by a sharp question on the [Camera-Type Detection PRD](../2026-Q2_camera-type-detection/PRD.md): we set acceptance rate as the success metric, but Yossi confirmed the current reality:

> The customer's email is on the appeal. The authority responds directly to **them**. Road Protect doesn't see the response. There's no per-fine outcome record. We can't compute acceptance rate, we can't notify the customer in our channels, and we can't learn which templates work.

This blocks:
1. **Measuring success of Camera-Type Detection** — the entire thesis is unmeasurable.
2. **VIP value proof** — we can't tell the user "we got your fine cancelled" because we don't know.
3. **Continuous improvement of templates** — no feedback loop.
4. **Future automation** — Phase 3 (auto-request "device card") and similar features all assume RP is in the response loop.

This is **foundational infrastructure**. Build it before Camera-Type Detection ships.

## Success metric

**% of submitted appeals where the authority's response is captured and tied to the correct fine, automatically.**

- Baseline: 0% (today, we have none).
- Target v1: ≥80% of appeals submitted post-launch.
- Stretch: ≥95% within 90 days.

The other thing this enables — acceptance rate measurement — is a downstream metric, not the success metric here. We're building the *pipe*, not the *number*.

## In scope

- [ ] Inbound email infrastructure under a dedicated subdomain (e.g., `appeals.roadprotect.co.il`)
- [ ] Per-appeal email alias generation: `appeal-{fine_id}@appeals.roadprotect.co.il`
- [ ] Submission flow updated to list the alias as primary contact (customer email kept as secondary in the appeal text)
- [ ] Inbound parser that extracts: outcome status, amount change, points change, free-text response, response date
- [ ] Per-fine `outcomes` record in the database
- [ ] Customer notification — WhatsApp + email + in-app status update, automatically, on parse
- [ ] Fallback: manual upload UI ("forward us the response") for any responses that don't arrive via the alias
- [ ] Operational dashboard showing inbound parse rate, parse confidence, and unparsed queue

## Out of scope

- **OAuth-based mail forwarding from customer's inbox** — Plan B fallback. Real cost-benefit not justified for v1. Phase 2 candidate.
- **Physical mail handling** — if the authority responds by paper letter only, we miss it. Out of scope; handled by the customer manually reporting back.
- **Authority-portal scraping** — there's no public API for police case management. Phase 3+.
- **Acceptance-rate dashboard UI for end users** — separate visualization project. This project produces the *data*.
- **Refund / re-appeal automation** when an appeal is rejected — separate logic, separate scope.

## Status & next action

- **Right now**: design doc drafted in `PRD.md`, awaiting Yossi review.
- **Next**: validate the legal/practical assumption that the appeal can list an RP-controlled email as contact. **This is the single blocker** — if it's not allowed, the whole design changes.
- **Blocked on**: legal/compliance call on "can the contact email on an appeal be different from the signatory's personal email?"

## Documents in this project

- `PRD.md` — design / characterization (three architecture options, picked one, data flow, schema)
- `SPEC.md` — technical spec (deferred until Yossi confirms direction)
- `decisions.md` — running log

## Decision log (in-flight)

- 2026-05-28 — Created as separate project (not bundled into Camera-Type Detection). Reason: foundational infra for multiple downstream projects, ships independently, different team likely involved (backend + email infra, not ML).

---

*When this ships, move to `../shipped/` and add `retro.md` with the measured parse-rate over 90 days.*
