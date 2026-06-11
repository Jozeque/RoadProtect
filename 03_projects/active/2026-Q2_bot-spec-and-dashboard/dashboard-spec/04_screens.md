# 04 — Dashboard Screens

*Screen-by-screen spec of the dashboard UI. The mockup in `mockups/dashboard.html` is the visual canonical reference; this doc is the behavior/data canonical reference.*

**Audience**: vendor (building the dashboard).
**RTL**: every screen is Hebrew RTL aligned right. English translation is a later pass.

---

## Global layout (all screens)

- **Language**: Hebrew
- **Direction**: RTL, content aligned right
- **Brand**: navy primary (#0d2548 approx, extract exact from roadprotect.co.il), white background, accents in the brand teal
- **Top bar**: logo right, page title center, time-window selector (7d / 30d / 90d / all) + date range picker left
- **Sidebar (right)**: navigation between screens
- **Loading state**: skeleton blocks, no spinner; data is paged for fast first paint
- **Empty state**: every zero-data block shows "אין נתונים בתקופה זו" with a faded icon

---

## Screen 1: Funnel Overview (סקירה כללית)

**URL path**: `/` (default landing)
**Purpose**: the at-a-glance "is the bot healthy" view — all scenarios visible, guardrails surfaced, can spot anomalies in 10 seconds.

### Above-the-fold blocks

**Block 1.1 — KPI cards (4-up row, RTL)**
- Total users reached (last window)
- Total converted (last window) + ₪ revenue
- Opt-out rate (red if >2%)
- Bad-feedback rate (red if >1%)

**Block 1.2 — "What needs my attention" banner**
- Shows any scenario currently failing guardrails (red list)
- Shows any pending human escalations past SLA (orange list)
- Empty state: "אין התראות כרגע ✓" in muted green

### Below-the-fold blocks

**Block 1.3 — C2B scenario funnels (one per scenario, 8 rows)**

Layout per row: a horizontal funnel-bar visualization, like:

```
C1 — קולד ליד     [████████░░░░░ 1,247] → [██░ 234] → [█ 89] → [▌ 31] → [▍ 24 → ₪9.8k]
                   reached         t1 reply   t2 reply   t3 reply   converted

                   opt-out: 1.2% ✓   bad-fb: 0.4% ✓   click to drill →
```

Hovering / clicking a bar → opens scenario drilldown (screen 2).

Numbers on each segment. Percentages on hover.

Row order: by reached count, descending. Or sortable.

**Block 1.4 — B1 inbound summary**

A separate panel below C2B:
- Sessions started (last window)
- Intent distribution (donut chart, 9 intents)
- Conversion rate
- Escalation rate

---

## Screen 2: Scenario Drilldown (פירוט תרחיש)

**URL path**: `/scenario/<code>` (e.g. `/scenario/C5`)
**Purpose**: deep view of a single C2B scenario.

### Block 2.1 — Header
Scenario code + name in Hebrew + audience description (from the spec) + active variants count.

### Block 2.2 — Full funnel (large)
Vertical funnel with all 8 steps:
1. Eligible (with `suppressed` footnote)
2. Reached
3. Touch 1 replied (% of reached)
4. Touch 2 sent
5. Touch 2 replied
6. Touch 3 sent
7. Touch 3 replied
8. Converted

Beside the funnel: drop-off rates between each step, colored:
- Green: drop-off lower than scenario's running average
- Yellow: roughly equal
- Red: drop-off higher than average (something's breaking)

### Block 2.3 — Conversion attribution
Pie/donut chart: of conversions, what % were attributed to each touch (1, 2, 3, organic). Drives "do we need touch 3 at all?" question.

### Block 2.4 — Variant breakdown
For scenarios with A/B variants: side-by-side funnels per variant. Helps Yossi pick winners.

### Block 2.5 — Top objections (last window)
Bar chart, sorted: which objections came up most? Pulled from `objection.raised` events.

### Block 2.6 — Reply samples
Scrollable list of 20 most recent replies to this scenario's touches. Each row:
- User first name + masked phone
- Touch (1/2/3)
- Reply text
- Branch the bot took
- Timestamp

(For privacy: phone masked unless user clicks "show".)

### Block 2.7 — Conversions list
Last 20 conversions in this scenario:
- User name + masked phone
- Plan converted to
- Revenue
- Touch attributed to
- Timestamp

### Block 2.8 — Guardrails strip
Mini cards:
- Opt-out rate (with sparkline trend, 30 days)
- Bad-feedback rate (with sparkline)
- Delivery failure rate
- Coupon redemption rate (if scenario uses coupons)

---

## Screen 3: Users Panel (משתמשים)

**URL path**: `/users`
**Purpose**: the "who" view. Yossi explicitly asked for: who replied to touch N, who flagged bad feedback, who opted out.

### Top filter strip

- **Filter by event type**: replied / converted / opted out / bad feedback / escalated / mid-sequence (toggle, can combine)
- **Filter by scenario**: C1..C7, B1, all
- **Filter by touch number**: 1 / 2 / 3 / all
- **Filter by time window**: 7d / 30d / 90d / all
- **Filter by subscription**: detection / trademobile_free / vip / lapsed / null
- **Search**: by name, phone, or reply text

### Main table

Columns:
| שם | טלפון | מסלול | תרחיש | אירוע | מספר נגיעה | תוכן תגובה / הקשר | תאריך |

Default sort: most recent first.

Pagination: 50 rows per page, infinite scroll optional.

Row actions:
- Click row → opens user-detail drawer (right-side panel) with full event history for that user, conversation transcript, and current state
- "פעולות" dropdown per row → manual actions: re-add to opt-out, force escalate, etc. (admin only)

### Export
"Export CSV" button — exports current filtered view. Includes a privacy note: "מידע אישי — לא לשתף מחוץ לארגון."

---

## Screen 4: Cohorts (קוהורטות)

**URL path**: `/cohorts`
**Purpose**: side-by-side comparison of how scenarios perform across different audience cohorts.

### Block 4.1 — Cohort picker
Up to 3 cohorts selected at once. Default: Trademobile-warm vs Cold-lead vs Lapsed.

### Block 4.2 — Side-by-side funnel grid
For each scenario (rows), 3 columns showing each cohort's funnel.

Easy-to-read color: highest-converting cohort in green, lowest in light red.

### Block 4.3 — Cohort-level KPIs
At top: each cohort's totals (reached, converted, conversion rate, revenue, opt-out rate, bad-feedback rate, ARPU).

### Block 4.4 — Acquisition-source mix over time
Stacked bar chart, last 90 days, showing volume of each cohort entering the bot weekly. Tells Yossi where his audience is coming from.

---

## Screen 5: Settings (הגדרות)

**URL path**: `/settings`
**Purpose**: Configure dashboard behavior.

- Time zone (default Asia/Jerusalem)
- Default time window
- Email digest schedule (daily / weekly / off)
- Guardrail thresholds (opt-out, bad-feedback) — admins can adjust
- Bot vendor stack info (for traceability)

---

## Mobile responsiveness

V1: dashboard is **desktop-first** (Yossi works on a laptop, this is an operational tool). Mobile fallback: read-only view of screen 1, no drill-down. Full mobile parity is v2.

---

## Permissions

V1: single internal user. Authentication via Google SSO (Yossi + team's @roadprotect emails).

No RBAC distinctions yet. V2 will add: admin (can configure thresholds, run manual actions) vs viewer (read-only).

---

## Accessibility

- All charts have a "show data table" toggle for screen readers
- Color isn't the only signal — guardrails also use icons (✓ / ⚠️) alongside colors
- Hebrew RTL throughout, including charts
- Keyboard navigation supported on table views

---

## Performance targets

- First paint < 1.5s on home (screen 1)
- Time-window switch < 800ms
- Drilldown navigation < 500ms
- Search in users panel < 300ms for 1000-row result

---

## Things deliberately not in v1

- Real-time alerting (email/Slack) — v2
- Custom queries / SQL view — v2 (probably never; surface via metrics if needed)
- A/B experiment management UI (start/stop, allocate traffic) — v2
- LTV cohort analysis (requires billing system integration) — v2
- Multi-language UI (English) — Q3+

---

## Open questions for Yossi

1. **Default time window**: 7d or 30d as the landing default? Recent activity favors 7d, but C6 (pre-expiry) cycles are 30 days so 30d shows more meaningful data.
2. **Phone masking by default**: my spec masks phone numbers in lists unless clicked. This is the privacy-safe default but means Yossi clicks once to get the contact info. Confirm OK.
3. **Daily digest email**: nice-to-have v1 or push to v2?
4. **Admin actions on user rows** (force-escalate, force-opt-out) — needed v1 or v2?
