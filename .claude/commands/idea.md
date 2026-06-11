---
description: Capture an idea fast. Usage — /idea [tag] <the idea>
argument-hint: [tag] <the idea>
---

Capture an idea in the Road Protect workspace.

The user's input: $ARGUMENTS

Steps:
1. Read `.claude/skills/roadprotect-pm/SKILL.md`.
2. Parse the input. If it starts with `[tag]`, use that tag; otherwise infer from the content (growth / product / pricing / bot / partnerships / ops / content / data).
3. Append a one-line entry at the **top** of `02_ideas/INBOX.md` (after the heading and instructions) in the format: `- YYYY-MM-DD | [tag] <idea>`.
4. If the idea is substantive (more than 25 words, or contains "let's", "we should", or hypotheses), also create `02_ideas/<kebab-name>.md` using `_TEMPLATE_idea.md` as the structure. Fill what you can, leave clear TODOs.
5. Then **push back**. Don't just file it. Ask: is this a real problem? Who has it? What's the cheapest test of the hypothesis?

One question, sharp. Then stop.
