# Decisions Log — Bot Spec v2 + Dashboard

Running log of choices made during this project. Newest at top.

---

### 2026-06-03 — Coupon logic corrected to match Yossi's chat decision (reverses the v2 ladder)
**Decision**: The only coupon is **`SAVE30` = 30% off the one-off appeal (₪49)**, issued **only in C7** (single-appeal abandoners). **No `SAVE50`, no 30%→50% ladder, no coupon on VIP, no high-LTV escalation.** C3 and C6 issue **no coupon** at all (their closers are value/urgency at full price). C7's goal is to complete the abandoned appeal; the VIP upsell is a separate, later flow (gradual conversion). Also: appeal-intent users route to the appeals department (052-586-6982) without re-collecting fine details.
**Reasoning**: The v2 spec (2026-05-26) had introduced a 30%→50% coupon ladder applied to VIP across C3/C6/C7. That directly contradicts Yossi's explicit decisions in the implementation chat (28/04–30/04): "we never agreed on 50%," the 30% is for the single appeal not VIP, VIP is already low-priced so don't discount it broadly, and conversion must be gradual (close the cheap appeal first, then upsell VIP). Surfaced when reconciling the scenarios against the chat feedback.
**Files touched**: `bot-spec/07_c7`, `03_c3`, `06_c6`, `08_b1`, `01_c1`, `00_overview`; `dashboard-spec/02_event_schema`, `03_funnel_model`; `docs/vendor-narrative`.
**Reversibility**: 🟡 the ladder could be reinstated, but only against Yossi's stated decision — would need his explicit reversal.

---

### 2026-05-26 — Multi-touch sequences over single-touch tightening
**Decision**: Every C2B scenario will be rewritten as a multi-touch sequence (touch 1 → optional touch 2 → optional touch 3 with delays + exit conditions), not just a tightening of the existing single-opener format.
**Reasoning**: The dashboard ask explicitly tracks "replied to message 1, message 2, message 3." That's a multi-touch funnel. Without sequences, the dashboard has nothing to show beyond a single row per flow, and we leave conversion on the table from users who would have converted on touch 2 with a different angle. Vendor also expects this — every modern WhatsApp drip platform supports sequences natively.
**Alternatives considered**:
- Single-touch + branches only (rejected — defeats the purpose of the dashboard ask)
- Multi-touch only for top 3 scenarios (rejected — inconsistent spec across scenarios is worse than uniform depth for a new vendor)
**Reversibility**: 🟡 expensive to reverse once vendor builds against this — sequences are core to the data model

---

### 2026-05-26 — Spec + Hebrew RTL HTML mockup for dashboard, not spec only
**Decision**: Dashboard deliverable is the full spec (metrics, events, funnel, screens) **plus** a working Hebrew RTL HTML/Tailwind mockup of the four screens.
**Reasoning**: Yossi wants to react to a visual before vendor builds. Markdown wireframes alone leave too much room for the vendor to ship something we don't want. The mockup is also a fast credibility signal in vendor pitches.
**Alternatives considered**:
- Spec only with markdown wireframes (rejected — Yossi explicitly chose mockup option)
- Mockup of just the hero screen (rejected — same reasoning, comprehensive mockup is the safer artifact)
**Reversibility**: 🟢 cheap to reverse — the mockup is HTML, easy to edit

---

### 2026-05-26 — Hebrew-first, English translation deferred
**Decision**: All bot copy in this spec stays in Hebrew. The wrapper / framework / dashboard spec text is English so the vendor can read it. Translation of Hebrew copy to English happens in a separate pass after the spec is frozen 100%.
**Reasoning**: Yossi explicit ask. Also: maintaining two languages in parallel during drafting doubles the surface for inconsistency. Lock one language, then translate.
**Alternatives considered**:
- Bilingual from the start (rejected — drift risk)
- English copy + Hebrew as a translation layer (rejected — Hebrew is the source of truth; the bot ships in Hebrew)
**Reversibility**: 🟢 cheap — adding English translation later is mechanical

---

### 2026-05-26 — One project folder, sub-folders for bot-spec and dashboard-spec
**Decision**: Single project `2026-Q2_bot-spec-and-dashboard/` with `bot-spec/`, `dashboard-spec/`, `mockups/` subfolders, rather than splitting into two projects.
**Reasoning**: The two halves only make sense together — the dashboard's event schema is derived from the bot's emission events, and the bot's "what counts as success" comes from the dashboard's funnel definition. Splitting forces cross-project references and risks one half drifting from the other.
**Alternatives considered**:
- Two projects (`2026-Q2_bot-spec-v2/` and `2026-Q2_bot-tracking-dashboard/`) (rejected — coupling outweighs the separation benefit)
**Reversibility**: 🟢 cheap — can split later if it gets unwieldy

---

### 2026-05-26 — Each scenario rewrite includes critique of the current version
**Decision**: Each rewritten scenario file in `bot-spec/` opens with a `## Critique of current version` block explaining what was weak in the original `06_bot/scenarios/c2b/0N_*.md` file before presenting the new version.
**Reasoning**: Yossi asked to "doubt the quality of the scenarios." Making the critique explicit (a) forces honest assessment instead of polite restatement, (b) gives the vendor context for why the new spec is shaped the way it is, (c) creates a paper trail Yossi can challenge.
**Alternatives considered**:
- Silent rewrite without critique (rejected — loses the "why this is better" signal)
- Critique as a separate doc (rejected — fragments the read)
**Reversibility**: 🟢 cheap — can strip the critique blocks when handing to vendor if they're distracting
