---
name: roadprotect-pm
description: Use whenever creating or editing anything inside 02_ideas/, 03_projects/, or 04_specs/ in the Road Protect workspace. Triggers on requests like "add idea", "spec the X feature", "write a PRD", "start a project", "plan the X rollout", "what should we work on next", "review the backlog". Keeps the PM artifacts consistent and rigorous — every idea has a hypothesis, every PRD has one success metric, every project has explicit out-of-scope.
---

# Road Protect PM Skill

How to write product-management artifacts in this workspace that are actually useful, not just well-formatted.

## Core principle

Bad PM docs are list-heavy, opinion-light, scope-creeping. Good PM docs:
- State a sharp problem
- Pick one success metric and own it
- Are explicit about what's *not* being done
- Make a recommendation, then defend it

When in doubt, write less, but make every section earn its place.

## When the user says "add idea: X"

1. Append a one-line entry to `02_ideas/INBOX.md` at the top:
   ```
   - YYYY-MM-DD | [tag] One-line idea description.
   ```
2. If the idea is substantive (>20 words of intent, or Yossi explicitly says "this is real"), also create `02_ideas/<short-kebab-name>.md` using `_TEMPLATE_idea.md` as the structure. Don't blindly copy the template — fill in what you have, leave clearly marked TODOs for what you don't.
3. After creating, push back on the idea: is this a real problem? what's the cheapest test? what would change Yossi's mind?

## When the user says "spec the X feature" or "start a project for X"

1. Determine: is this a new project, or are we updating an existing one?
2. For new: create `03_projects/active/YYYY-Q#_<short-name>/` and copy the contents of `03_projects/_template/`.
3. Fill in `README.md` first (the entry point). Then fill in `PRD.md`. Don't start with `SPEC.md` — engineering specs come after product is clear.
4. **Hard rules for the PRD:**
   - **Problem**: a real, observable problem. If you can't name who has it and how often, push back.
   - **Target user**: ONE segment, narrow. Not "all drivers." Reference `06_bot/personas/PERSONAS.md` when relevant.
   - **Hypothesis**: written as "we believe X will cause Y for Z; we'll know if W within T."
   - **Success metric**: ONE number. Define baseline + target. Not a list.
   - **Out of scope**: must be filled in. Empty out-of-scope = scope-creep guaranteed.
5. After drafting, ask Yossi one sharp question: what's the riskiest assumption in this PRD?

## When the user says "what should we work on next?" or "review the backlog"

Don't dump the whole inbox. Do:

1. Read `02_ideas/INBOX.md` and any flagged-as-ready ideas.
2. Read `03_projects/active/` to see what's in-flight.
3. Rank top 3 by your assessment of: **impact × strategic fit ÷ effort**.
4. Present with reasoning: "I'd prioritize A because [reasoning], over B because [trade-off]."
5. Be opinionated. Pick.

## When writing a decision log entry

Format:

```markdown
### YYYY-MM-DD — [decision title]
**Decision**: What was decided.
**Reasoning**: The 1–3 reasons that drove it.
**Alternatives considered**: A (rejected because…), B (rejected because…).
**Reversibility**: 🟢 cheap to reverse | 🟡 expensive to reverse | 🔴 one-way door.
```

One-way doors get extra scrutiny — flag them.

## Tone in PM docs

- First-person plural ("we") when describing what Road Protect will do.
- Direct, declarative sentences. "We will ship X." Not "We are considering possibly shipping X."
- Avoid hedging adjectives ("various," "several," "potentially").
- Israeli/founder voice — pragmatic, not corporate.

## What NOT to do

- Don't generate PRDs that read like ChatGPT output (over-bulleted, hedged, padded).
- Don't claim user numbers or metrics that aren't documented in `09_metrics/`.
- Don't pull "industry best practice" claims without a source.
- Don't ship the PRD without explicit "what's out of scope" filled in.

## Quick reference — file structure

```
02_ideas/
├── INBOX.md                          ← fast capture, newest at top
├── _TEMPLATE_idea.md                 ← scaffold
└── <kebab-name>.md                   ← expanded ideas

03_projects/
├── _template/                        ← copy this for new projects
│   ├── README.md
│   ├── PRD.md
│   ├── SPEC.md
│   ├── decisions.md
│   └── mockups/
├── active/<YYYY-Q#_name>/
├── shipped/<YYYY-Q#_name>/
└── archived/<YYYY-Q#_name>/

04_specs/                             ← cross-referenced specs (rare; usually live inside project)
```
