# C3 — Past Customer Winback

**Channel**: WhatsApp (C2B agent, outbound)
**Audience**: Lapsed users with detected fines
**Goal**: Reactivate, push to VIP
**Tone**: Service-first ("we're still finding fines for you"), then upsell

## Trigger

User with prior subscription (now expired or cancelled), system has detected ≥2 fines since their lapse.

## Variables

- `{{name}}` — from `$json.name`
- `{{fines}}` — fine count

## Opening message

General post-expiry body (C2 now diverges — it adds an explicit Trademobile free-year reference for that cohort; C3 stays Trademobile-agnostic):

```
היי {{name}}, כאן Road Protect 🛡️

המערכות שלנו איתרו עבורך {{fines}} דוחות בתקופה האחרונה, וחשוב לנו לוודא שהם לא נשארים ללא טיפול.

כדי למצות את הזכויות שלך ולחסוך בנקודות וכספים מיותרים, אנחנו מזמינים אותך לעבור למסלול המלא שלנו. שם נוכל להעניק לך ליווי מקצועי מקצה לקצה וטיפול בירוקרטי מלא בכל דוח שאותר.

מעניין אותך לשמוע על היתרונות של המסלול המלא והשקט שהוא ייתן לך? אני סוכן AI דיגיטלי ואפשר לשאול אותי כל שאלה 🛡️
```

## Relationship to C2

Both audiences are "warm + has fines," but they're no longer identical: C2 references the Trademobile free year explicitly (required for that cohort); C3 is the general lapsed-customer version with no Trademobile framing. A lapsed customer who originally came via Trademobile *and* whose account is now expired sits between the two — see open questions.

## Branches

(Same as C2.)

## Open questions / opportunities

1. **Lapsed users should probably get a different angle**: acknowledge the lapse, possibly offer a coupon (currently only the "Dirty & Quick" scenario C7 does this). Worth A/B testing.
2. **Time-since-lapse should affect tone**: <30 days = "wanted to catch you before too much builds up"; >90 days = "your protection has been off, here's what's accumulated."
3. **A re-onboarding gentle flow** might convert better than a direct VIP pitch for users who lapsed >6 months ago.

→ Idea candidate: `02_ideas/lapsed-user-tiered-winback.md` (TODO)
