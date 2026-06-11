---
name: bot-scenario-author
description: Use whenever creating, editing, or extending bot scenarios in 06_bot/scenarios/ — the WhatsApp C2B (outbound) or B2C (inbound) AI agents. Trigger phrases include "write a new bot scenario", "draft a flow for [trigger]", "extend the [scenario] with [branch]", "what should the bot say when [situation]", "build a winback flow". Keeps new flows consistent with the existing structure, the brand voice, the legal line, and the gender-detection pattern.
---

# Bot Scenario Author Skill

How to author or modify WhatsApp bot flows for Road Protect's C2B and B2C agents.

## Read first

Before writing anything in `06_bot/scenarios/`, glance at:

1. `06_bot/scenarios/INDEX.md` — list of existing scenarios, principles, naming
2. `06_bot/knowledge_base/voice_and_tone.md` — how the bot sounds
3. `06_bot/knowledge_base/objection_library.md` — canonical pushback responses
4. `06_bot/personas/PERSONAS.md` — who you're writing to
5. `01_business_context/LEGAL_DISCLAIMER.md` — what you cannot say

Also check the existing scenarios for the format — every new flow should match their structure.

## Scenario file structure

Every scenario lives at `06_bot/scenarios/c2b/<NN>_<short-name>.md` or `06_bot/scenarios/b2c/<NN>_<short-name>.md` and follows this structure:

```markdown
# [Cn or Bn] — [Short title]

**Channel**: WhatsApp ([C2B agent, outbound | B2C agent, inbound])
**Audience**: [exact segment definition — who fires this]
**Goal**: [the one outcome we want]
**Tone**: [a sentence describing tone]

## Trigger
[Exact event/condition that fires this scenario]

## Variables
[Templated tokens used in the flow, with source]

## Opening message
\`\`\`
[The Hebrew text the user sees, exactly as it will be sent]
\`\`\`

## Branches
### B1 — [user reply pattern]
[response]

### B2 — [another reply pattern]
[response]

## Gender detection / handling
[How the bot handles M/F register switching, if relevant]

## Things to be careful about
[Legal-line concerns, tone risks, common mistakes]

## Open questions
[Anything that needs Yossi to clarify before this can go live]
```

## When asked "write a new bot scenario for [trigger]"

1. **Diagnose the audience first.** Which persona? (See `personas/PERSONAS.md`.) If the trigger doesn't map cleanly to a persona, push back and propose a new persona before writing.
2. **Decide C2B (outbound) or B2C (inbound).** Different files, different folders.
3. **Pick the next sequential number** — C8, B2, etc.
4. **Write the opening message in Hebrew.** Match voice and tone. Don't translate English drafts; compose natively.
5. **Anticipate 2–4 branches.** What will users actually reply? Cover at least: the positive ("tell me more"), the deflection ("not now / not interested"), and the question-back ("how does it work / who are you").
6. **Add the gender-detection rule** if the flow involves enough exchange to detect.
7. **Update `06_bot/scenarios/INDEX.md`** with a row for the new scenario.

## The opening-message checklist

Before declaring an opening message done, verify:

- [ ] Starts with personalized greeting (`היי {{name}}`) when name is available
- [ ] Identifies brand ("Road Protect" / "כאן Road Protect") within the first paragraph
- [ ] States the *reason* for the contact in 1 sentence
- [ ] Provides value or context (don't go straight to the pitch)
- [ ] Ends with a clear next step — usually a question or a CTA
- [ ] Includes "אני סוכן AI דיגיטלי" or equivalent if disclosing AI identity (required for cold/outbound)
- [ ] Max 1–2 emojis (🛡️ is the brand default)
- [ ] No legal-line violations (see `LEGAL_DISCLAIMER.md`)
- [ ] Max 6 short paragraphs; split if longer

## Gender-detection pattern

Default: gender-neutral pronouns ("ברצונך", "עבורך", "שלך"). 

When the user replies:

- If reply contains masculine verb forms ("מעוניין", "אני יודע", "אני רוצה" + masculine adjective) → lock masculine.
- If reply contains feminine verb forms ("מעוניינת", "אני יודעת", "אני רוצה" + feminine adjective) → lock feminine.
- If ambiguous → stay neutral until the next reply.

Write both branches when the response would otherwise read awkwardly. Don't try to be clever with double-form ("יקר/ה") inside emotional copy — it kills the warmth.

## What every new scenario must NOT do

- Promise lawyer representation
- Promise guaranteed cancellation
- Quote uncited success rates ("85% of fines are cancelled")
- Claim instantaneous response times without data
- Use coupons outside the explicit winback/abandonment contexts (C7-style)
- Open with "We hope you're having a wonderful day"

## Updating the INDEX

After creating a new scenario, append a row to `06_bot/scenarios/INDEX.md`:

```markdown
| Cn | [trigger description] | [audience] | `c2b/NN_filename.md` |
```

Keep the table sorted by scenario number.

## When asked to extend an existing scenario

1. Open the existing file.
2. Identify whether the extension is a new branch (add under `## Branches`) or a new variant of the opening (add under a `## Variant B` section with rationale for when to use which).
3. Maintain the same voice and structure as the existing content.
4. If the extension changes the scenario's goal or audience, that's a new scenario, not an extension — push back.

## Sanity check before declaring done

Read the scenario back. Ask:

1. Would a real Israeli driver who got this message feel respected, or sold-to?
2. Is the legal line clean throughout?
3. Are the branches realistic — would real users actually reply this way?
4. Is the success signal clear (what would indicate this scenario worked)?
5. Did I update INDEX.md?
