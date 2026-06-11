# Camera-Type Detection (Phase 1 of Camera-Aware Appeal Engine)

**Status**: 🟡 specing
**Owner**: Yossi
**Started**: 2026-05-28
**Target ship**: 2026-Q3 (8–10 weeks from kickoff)
**One-line**: Auto-detect enforcement-camera type from uploaded fines and route to a camera-specific appeal template.

---

## Why this exists

Triggered by reading the [Mitsu enforcement-tech articles](https://www.mitsu.co.il/?page_id=1681) on 2026-05-28. Two facts surfaced that make a generic appeal template a strategic mistake:

1. **The April 2025 Ashdod ruling on Gatso A-3** — courts must subtract 9 km/h from A-3 readings, and the EV-interference argument creates a separate non-discrimination problem. Any A-3 fine from 2025 onward is appealable on those specific grounds — but a generic template does not invoke them.
2. **Different camera technologies have different legal failure modes**: LTI 20-20 (ממל"ז) has the 2–3-second lock window and calibration certificates; Bee III (דבורה) requires eye contact + immediate stop; A-3 has the Ashdod ruling. One template ≠ optimal appeal.

Today the RP appeal pipeline produces one draft regardless of which device issued the fine. Acceptance rate is the most direct lever on VIP value.

## Success metric

**Appeal acceptance rate** for camera-issued fines processed by Road Protect.
- Baseline: TBD (open question — we don't have this number in `09_metrics/`).
- Target: meaningful uplift — we'll define the exact target once baseline is known. Internal hypothesis: +5–10 percentage points.

## In scope

- [ ] OCR / NLP on uploaded fine images and PDFs to extract structured fields: **camera type, location text, measured speed, speed limit, violation type, date/time, fine amount**.
- [ ] Camera-type classifier (rule-based first; ML if data justifies) producing one of: **Gatso A-3, LTI 20-20 / ממל"ז, Bee III / דבורה, Red-light, Parking, Officer-stopped, Unknown**.
- [ ] Four new appeal templates (A-3 / ממל"ז / דבורה / Red-light). One existing template kept as fallback for Unknown.
- [ ] EV / hybrid flag — cross-reference the user's registered vehicle. A-3 fine + EV/hybrid plate → "high-confidence appeal" badge in UI.
- [ ] Internal review tool — human reviewer can override classifier decision before draft is sent to user. Reviewer feedback feeds the classifier.

## Out of scope

- **Camera-location database (Phase 2)** — mapping each fine to a specific camera ID and its calibration history. Different project.
- **Auto-request of "device card" / כרטיס המכשיר from police prosecution (Phase 3)** — depends on a working integration with police case-management. Different project, possibly different vendor.
- **Officer-stopped tickets** — kept on the generic template. Different appeal logic (witness-based, not device-based).
- **Municipal parking fines** — different domain (no enforcement-device argument). Generic template stays.
- **Non-Hebrew tickets** — there are no Hebrew/English mixed tickets in real practice. Skipping ML on translated OCR.
- **Re-processing historical closed appeals** — only forward-looking. Retroactive sweep of A-3 fines is a separate project we already discussed (see decisions.md).

## Status & next action

- **Right now**: PRD drafted, awaiting Yossi review.
- **Next**: Yossi reviews PRD, surfaces the riskiest assumption, and decides whether this becomes the Q3 build commitment.
- **Blocked on**: baseline acceptance rate number (need from `09_metrics/` or from RP engineering team).

## Documents in this project

- `PRD.md` — product requirements
- `SPEC.md` — technical spec (deferred until PRD is approved)
- `decisions.md` — running decision log
- `mockups/` — to be added when reviewer UI is specced
- Related: `../../05_mockups/benefits-app-listing/` (unrelated project, but uses adjacent assets)

## Decision log (in-flight)

- 2026-05-28 — Split the original "Camera-Aware Appeal Engine" idea into three phases. This project is Phase 1 only. Phases 2 & 3 will be separate projects after Phase 1 ships and shows uplift.

---

*When this ships, move to `../shipped/` and add `retro.md` with the 90-day measured uplift.*
