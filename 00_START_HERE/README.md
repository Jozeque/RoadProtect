# Start Here

Welcome to the Road Protect PM workspace. If you're a fresh Claude session, read `../CLAUDE.md` first, then this, then `../01_business_context/COMPANY_BRIEF.md`.

If you're Yossi and you've come back after a break, here's the lay of the land in 30 seconds:

## What this workspace is

A local-first PM and strategy environment for Road Protect. Everything lives in markdown so you (and any Claude session) can reason over it. The structure is split into:

- **Context** (`01_business_context/`) — the canonical facts. Don't rewrite copy that contradicts these.
- **Backlog** (`02_ideas/`) — running list of ideas, one file per substantive one, plus a fast-capture `INBOX.md`.
- **Projects** (`03_projects/`) — anything you're actively building or have specced. Three states: active, shipped, archived.
- **Specs** (`04_specs/`) — formal PRDs and tech specs. Usually owned by a project but kept centrally for cross-reference.
- **Mockups** (`05_mockups/`) — UI mockups. One folder per feature, single-file HTML for portability.
- **Bot** (`06_bot/`) — the WhatsApp agents (C2B + B2C), scenarios, personas, knowledge base.
- **Marketing** (`07_marketing/`) — campaigns and copy.
- **Research** (`08_research/`) — competitors, users, market.
- **Metrics** (`09_metrics/`) — KPIs and dashboards.

## Three things to do on day 1

1. **Fill in real numbers**. Open `09_metrics/KPIs.md` and replace the placeholders with real MRR, churn, conversion data. The whole workspace gets sharper once the numbers are real.
2. **Verify the bot scenarios**. The Hebrew scenarios I extracted from your PDF are in `06_bot/scenarios/`. Eyeball them — fix anything I mis-OCR'd.
3. **Pick the top 3 priorities** for the next 90 days and create project folders for them in `03_projects/active/`.

## How to start a session with Claude Code

From inside this folder, just `claude` (or `claude-code`). The `CLAUDE.md` auto-loads. Then say:

- "What are we working on today?" — for a status check
- "Spec the [feature]" — to start a new project
- "Mockup the [screen]" — for a UI mockup
- "Write a bot scenario for [trigger]" — for a new agent flow
- "Add idea: [idea]" — to drop into the INBOX

## Skills installed

- `roadprotect-pm` — PRDs, ideas, project structure
- `hebrew-rtl-content` — Hebrew marketing/copy
- `bot-scenario-author` — new WhatsApp agent flows

These auto-load. You don't need to invoke them by name.
