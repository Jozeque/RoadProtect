# Decision Log

Newest at top. One entry per non-trivial decision.

## Format
```
### YYYY-MM-DD — [decision title]
**Decision**: What was decided.
**Reasoning**: Why.
**Alternatives considered**: A, B (and why rejected).
**Reversibility**: 🟢 cheap to reverse | 🟡 expensive to reverse | 🔴 one-way door.
```

---

### 2026-05-28 — Split Camera-Aware Appeal Engine into 3 phases; ship Phase 1 alone
**Decision**: This project covers only camera-type detection + camera-specific templates (Phase 1). Phases 2 (camera-location DB) and 3 (auto-request of "device card" from police prosecution) are deferred to separate projects.
**Reasoning**:
1. Phase 1 is buildable in 8–10 weeks with existing infrastructure (OCR + classifier + 4 templates). Phases 2–3 require external data and police integrations — months of additional work and partner dependencies.
2. Phase 1 already produces measurable acceptance-rate uplift if the hypothesis holds. We don't need Phases 2–3 to validate the thesis.
3. Bundling them all delays the value and increases risk of cancellation due to scope.
**Alternatives considered**:
- A: Build all three together — rejected, scope too large, timeline too long for one go.
- B: Build only the A-3 template, skip the classifier — rejected. Then we'd need humans to manually tag every fine. Doesn't scale and doesn't justify engineering investment.
**Reversibility**: 🟢 cheap to reverse. If Phase 1 underperforms, we revert via feature flag.

---

### 2026-05-28 — Hard dependency on Appeal Outcome Tracking project
**Decision**: This project cannot ship its full value (measurable acceptance-rate uplift) until the [Appeal Outcome Tracking](../2026-Q2_appeal-outcome-tracking/) project is in production. The two are sequenced: outcome tracking first, camera-type detection second.
**Reasoning**: Confirmed by Yossi 2026-05-28 — today the authority responds to the customer's personal email and RP has zero visibility. Without outcome capture, we cannot measure whether camera-specific templates outperform the generic one.
**Alternatives considered**:
- Ship Camera-Type Detection in parallel and measure later — rejected, because the templates would go live without any feedback loop.
- Hand-track outcomes manually for the pilot cohort — possible but doesn't scale and biases the pilot. Use only if Appeal Outcome Tracking slips badly.
**Reversibility**: 🟢 cheap — it's a sequencing decision, not a code commitment.

---

### 2026-05-28 — Don't include retroactive A-3 sweep in this project
**Decision**: The retroactive sweep of existing fines that already had appeals submitted with the old generic template is a separate project, not bundled into this PRD.
**Reasoning**:
1. The retroactive sweep is operations/marketing-led (WhatsApp outreach to existing users), not engineering-led. Different team, different ROI calculation.
2. It can launch before this PRD ships — doesn't depend on the new pipeline. Acting fast on it has its own urgency (fines age out).
3. Bundling muddies the success-metric measurement here.
**Alternatives considered**:
- A: Bundle them — rejected, see above.
**Reversibility**: 🟢 cheap to reverse — we can always add it back.
