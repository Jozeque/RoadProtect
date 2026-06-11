---
description: Start a new project. Usage — /new-project <short-name> <one-line description>
argument-hint: <short-name> <one-line description>
---

Start a new Road Protect project.

The user's arguments: $ARGUMENTS

Steps:
1. Read `.claude/skills/roadprotect-pm/SKILL.md` first.
2. Parse the user's arguments: first token is the short name (kebab-case), the rest is the one-line description.
3. Create a folder under `03_projects/active/` named `YYYY-Q#_<short-name>/` (use current date for YYYY-Q#).
4. Copy the entire contents of `03_projects/_template/` into the new folder.
5. Fill in `README.md`: name, status (`🟡 specing`), owner (Yossi), started date, the one-line description.
6. Open the PRD and fill in just the title and date — leave the rest scaffolded.
7. Tell me what was created, then ask me **one** sharp question: who is the target user for this and what's the success metric I'm chasing?

Don't write the whole PRD on your own — that's the next conversation.
