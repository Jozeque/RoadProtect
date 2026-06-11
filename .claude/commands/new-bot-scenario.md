---
description: Draft a new WhatsApp bot scenario. Usage — /new-bot-scenario <trigger description>
argument-hint: <c2b|b2c> <trigger description>
---

Draft a new bot scenario for one of Road Protect's WhatsApp agents.

The user's input: $ARGUMENTS

Steps:
1. Read `.claude/skills/bot-scenario-author/SKILL.md` first.
2. Then read `06_bot/scenarios/INDEX.md` to see existing scenarios and pick the next number.
3. Read `06_bot/knowledge_base/voice_and_tone.md` and `06_bot/personas/PERSONAS.md`.
4. Parse the input: first token should be `c2b` or `b2c`; the rest is the trigger description.
5. Map the trigger to a persona (or push back if no clean fit).
6. Create the scenario file at `06_bot/scenarios/<c2b|b2c>/NN_<kebab-name>.md` using the structure in the SKILL.
7. Write the opening message in **Hebrew** (don't translate from English drafts), with personalization tokens.
8. Anticipate 2–4 user reply branches and write responses for each.
9. Update `06_bot/scenarios/INDEX.md` with the new row.
10. Ask me to review the opening message in particular — that's the highest-leverage piece.
