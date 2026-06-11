---
description: Create a UI mockup. Usage — /mockup <feature> <what to show>
argument-hint: <feature-name> <description of the screen>
---

Create a UI mockup for a Road Protect screen or component.

The user's input: $ARGUMENTS

Steps:
1. Read `/mnt/skills/public/frontend-design/SKILL.md` first.
2. Then read `.claude/skills/hebrew-rtl-content/SKILL.md` for the Hebrew/RTL rules and brand colors.
3. Parse the input: feature name (kebab-case) and what to show.
4. Create the folder `05_mockups/<feature-name>/` if it doesn't exist.
5. Build a **single HTML file** (`index.html`) with:
   - `<html dir="rtl" lang="he">`
   - Tailwind via CDN
   - Hebrew text throughout
   - Road Protect brand colors (navy primary, white background, accent reds/oranges for fine-alerts, greens for protected/success)
   - Realistic content — use plausible Hebrew names, fines, dates, amounts. Not Lorem Ipsum.
   - Mobile-first responsive
6. After creating, briefly describe what's in the mockup and ask: does this match what I had in mind, or should we iterate?

Don't over-design. Aim for "looks like a real Road Protect screen" not "art-directed concept."
