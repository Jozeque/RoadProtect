# PRD: [Project Name]

**Status**: 📝 draft | ✅ approved | 🔒 frozen
**Author**: Claude (drafted) / Yossi (approved)
**Last updated**: YYYY-MM-DD
**Version**: 0.1

---

## 1. Problem

A short, sharp statement of the problem we're solving. Include: who has it, when, how often, and what they do today instead.

## 2. Target user

The single user segment we're optimizing for. If you're tempted to write "everyone" or "all drivers," stop and narrow.

Example: "Trademobile car buyers who are in months 9–12 of their free Detection year and have had at least one fine detected during that year."

## 3. The hypothesis

We believe that **[change X]** will cause **[outcome Y]** for **[segment Z]**.
We'll know we're right if **[signal]** within **[time window]**.

## 4. Success metric (the one number)

The primary metric. Define how it's measured, the baseline, and the target.

## 5. Secondary metrics & guardrails

- Secondary: [e.g. NPS, support ticket volume, unsubscribe rate]
- Guardrail: [e.g. "must not increase complaint-to-message ratio above X%"]

## 6. User journey / flow

Describe the user experience step by step. For bot flows, include the trigger, the first message, and the branch logic. For UI, walk through the screens. Link to mockups.

## 7. Requirements

### Must have (v1 ships without these = no go)
- [ ] R1
- [ ] R2

### Should have (v1.1 or fast-follow)
- [ ] R3

### Won't have (this round)
- R4 — explicitly deferred

## 8. Edge cases & error states

- What if [edge case]?
- What if [error state]?
- What if [adversarial user behavior]?

## 9. Legal / compliance review

Anything that touches: the legal disclaimer, payment flow, data we collect, communications consent, GDPR/Israeli privacy regulation. List specifically.

## 10. Rollout plan

- Internal test → soft launch (e.g. 5% of cohort) → full launch.
- Success criteria to graduate between stages.
- Rollback plan if metrics go red.

## 11. Open questions

- ?
- ?

## 12. Out of scope (saying it again because it always matters)

Reiterate what we are *not* doing this round.

---

*PRD owned by Yossi. Engineering / vendor reads this and produces the tech spec in `SPEC.md`.*
