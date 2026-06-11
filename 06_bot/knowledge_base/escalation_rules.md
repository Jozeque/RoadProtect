# Escalation Rules

When the bot stops handling the conversation and hands off to a human agent.

## Always escalate (no exceptions)

1. **User explicitly asks for a human.** "אני רוצה לדבר עם נציג / מישהו אמיתי / בנאדם" — hand off immediately. Don't try to convince them to stay with the bot.
2. **Legal threat.** Any mention of "תביעה", "עורך דין שלי", "משטרה", "תלונה" against Road Protect.
3. **Refund / dispute on a paid case.** Routes to support, not sales.
4. **Death / serious illness in family.** Mentions of bereavement / hospitalization / etc. — human empathy required.
5. **Complaint about how the bot itself behaved.** ("הסוכן שלכם הציק לי / שיקר לי")
6. **Mental-health flag.** Anything suggesting distress beyond normal annoyance (self-harm, financial crisis, etc.). Human routing + adjusted tone.

## Escalate after one attempt

7. **Technical issue specific to their account.** Bot can try once ("בוא ננסה ביחד — מה בדיוק קרה?"). If not resolved → human.
8. **Question about an active appeal in progress.** Refer to the team handling the appeal.
9. **Repeated misunderstanding** — bot misunderstood the user 2+ turns in a row.

## Don't escalate

10. **Simple pricing / product questions.** That's bot territory.
11. **Standard objections.** Use `objection_library.md`.
12. **Common factual questions.** Use `faq.md`.
13. **Hesitation / "let me think."** Leave the door open, don't escalate.

## Cancellation / plan-change requests

Not a human escalation — handle inline. When a user wants to **cancel or change their plan** (including the free Trademobile subscription), route them to email:

```
אין בעיה. כדי לבטל או לעדכן את המסלול, שלח/י מייל ל-info@roadprotect.co.il ונטפל בזה בהקדם 🙂
```

There's a self-serve cancel on the site but no upgrade/downgrade trigger yet, so email is the path for now (decision: Yossi/team, 12/04). Don't try to talk the user out of cancelling — if they're firm, give the email cleanly.

## Human-handoff contacts

When a case genuinely needs a human (per the rules above), route to:

- **General / support**: info@roadprotect.co.il
- **Appeals (active appeal, appeal grounds, status)**: appeal@roadprotect.co.il — or the appeals WhatsApp **052-586-6982**
- **Urgent / needs a person now**: Yossi's WhatsApp **058-794-4611**

Cases where the bot can't actually resolve the issue (e.g. a user disputing the appeal grounds we filed) must reach a human — don't let the bot improvise an answer it can't stand behind (Yossi, 27/04).

## Handoff message (canonical)

```
אעביר אותך עכשיו לנציג שלנו ויחזרו אליך בהקדם. בינתיים אני כאן אם יש משהו אחר שאני יכול לעזור איתו 🛡️
```

## Handoff metadata

When handing off, the bot should send the human agent a structured summary:

- **User ID / phone**
- **Conversation history** (last 5 turns)
- **Detected intent** (what triggered the escalation)
- **Urgency** (high if legal threat / mental-health flag / dispute; medium if account-specific; low otherwise)
- **Suggested first response** from the bot's POV

## SLA targets

- Legal threats / mental-health flags: **<30 minutes**, business hours only (extend handling rules outside hours)
- Refund / dispute: **<2 business hours**
- Technical / appeal status: **<4 business hours**
- General "wanted to talk to a human": **<1 business day**

## Open questions for Yossi

- Is there an actual human-handoff endpoint, or is escalation = WhatsApp ping to the team's shared inbox?
- Outside business hours — does the bot say "ours hours are X-Y" or just route into a queue?
- What's the current escalation rate? (If >15% of conversations escalate, the bot is under-handling. If <2%, the bot may be over-handling and frustrating users.)
