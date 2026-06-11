# Glossary

Internal terms, Israeli traffic-domain terms, and product-surface names. Keep this updated; new contributors and new Claude sessions both reference it.

## Product surfaces

| Term | Meaning |
|---|---|
| **Detection** | The basic ₪99/year plan. 24/7 fine radar + alerts, no appeal handling. |
| **VIP** | The ₪489/year flagship plan. Detection + unlimited appeal handling + late-fee absorption + lawyer referral. |
| **One-off** | The ₪49 single-appeal pay-as-you-go option. |
| **Radar** | Internal term for the monitoring engine that scans authority databases. |
| **Alert** | The WhatsApp + email notification triggered when a fine is detected. |
| **Appeal** | The legal document drafted by the system and submitted by the user contesting a fine. |
| **Fine verification** | The `/fine-verification` surface — drivers check whether they have an outstanding fine. Discovery wedge. |
| **The magazine** | `/magazine` content hub. SEO + reform-awareness play. |

## Israeli traffic / legal domain

| Hebrew term | English | What it means in practice |
|---|---|---|
| דוח | "doh" — a fine / ticket | The unit. Parking, traffic camera, moving violation, etc. |
| ריבית פיגורים | Late-payment interest | The automatic **50% surcharge** on an unpaid fine after its due date. |
| כפל קנס | "kefel knas" — fine doubling | The automatic doubling of fines once a driver accumulates 4+ unhandled fines in 3 years. |
| נקודות | Points | License points. Accumulate → mandatory defensive driving course → suspension. |
| הליך מנהלי | Administrative procedure | The post-reform process: no court, documents only. |
| ערעור | Appeal / contestation | The challenge filed to cancel a fine. |
| מצלמת אכיפה | Enforcement camera | Speed / red-light / bus-lane camera. |
| נת״צ | Bus lane | Public-transit lane. Common violation. |
| משטרת ישראל | Israel Police | The national-level authority for moving violations. |
| עירייה / רשות מקומית | Municipality / local authority | Issuer of parking fines and some local moving violations. |
| נהיגה מונעת | Defensive driving (course) | Mandatory course triggered at a points threshold. |

## Bot / CRM terms

| Term | Meaning |
|---|---|
| **C2B agent** | Outbound WhatsApp agent that initiates conversations (cold list, Trademobile warm list, churned users). |
| **B2C agent** | Inbound WhatsApp agent that handles user-initiated conversations and post-alert reactions. |
| **Cold list** | Leads who left details previously but never converted. |
| **Trademobile warm list** | Used-car buyers who got 1 free year of Detection through the Trademobile partnership. |
| **Churned / lapsed** | Users whose free year or paid subscription expired without renewal. |
| **Dirty & Quick** | Internal name for the aggressive winback flow (coupon-led, urgency-led). See bot scenarios. |
| **Scenario** | A scripted bot flow with branches. Lives in `06_bot/scenarios/`. |
| **Persona** | A categorization of the user receiving messaging. Lives in `06_bot/personas/`. |

## Partner / channel shorthand

| Term | Meaning |
|---|---|
| **Trademobile** | Used-car platform. Bundles 1 year of Detection with every car purchase. Primary warm channel. |
| **Pango** | Parking-payments app. Cross-promo partner. |
| **B2B / fleet** | Enterprise customers managing fleets — Strauss, Touch, Samelet, Tir, Leasecom, Akiva, Ashkelon municipality. |
