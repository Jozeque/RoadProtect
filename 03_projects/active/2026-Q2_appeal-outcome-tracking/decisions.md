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

### 2026-05-28 — Picked Option A (RP-owned alias per fine) over OAuth and manual-only paths
**Decision**: Primary capture is via `appeal-{fine_id}@appeals.roadprotect.co.il`. Manual upload (Option C) is the fallback for missed cases. OAuth (Option B) deferred to Phase 2.
**Reasoning**:
1. Option A is the only design with 100% attribution-by-construction — `fine_id` lives in the email address itself, no parsing needed.
2. Customer experience is materially better — parsed, in-app, branded — vs. raw authority email.
3. Foundation for all downstream automation (Phase 3 device-card requests, etc.).
4. OAuth (B) tops out at ~85% coverage and has high onboarding friction. Not worth the complexity for v1.
**Alternatives considered**:
- B (OAuth forwarding) — rejected for v1; coverage cap + sensitive scope + per-provider implementation complexity. Revisit in Phase 2.
- C alone (manual upload) — rejected; biased data (rejection-correlated silence), low response rate.
**Reversibility**: 🟡 expensive to reverse — once authorities have appeals submitted with our aliases, those aliases must remain active for the response window. Switching strategies mid-flight means running both for 90+ days.

---

### 2026-05-28 — Treat this as foundational infra, not bundled with Camera-Type Detection
**Decision**: Split into its own project even though it was discovered through the Camera-Type Detection PRD's open questions.
**Reasoning**:
1. Many future RP projects depend on having an outcome record per fine — not just Camera-Type Detection.
2. Different engineering skill set (backend + email infra vs. ML/OCR).
3. Can ship independently; Camera-Type Detection can't ship usefully without it, but this can ship before Camera-Type Detection is ready.
4. Bundling would have created an artificial dependency in the wrong direction.
**Alternatives considered**:
- Add it as a phase to Camera-Type Detection — rejected, see above.
**Reversibility**: 🟢 cheap to reverse — just a project-organization choice.
