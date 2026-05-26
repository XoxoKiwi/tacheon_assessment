# Orbit — Product Brief
**Internal Marketing Performance Insights Tool**  
*Tacheon Assessment — Task 1: Product Scoping*

---

## 1. Product Overview

Orbit is an internal operational analytics workspace designed for marketing teams that manage multiple D2C client brands. It answers one recurring question — *"How is our marketing performing across channels right now, and where should we be focusing?"* — without anyone having to manually pull, stitch, or reformat data.

Orbit is not an AI copilot. It is not a client-facing dashboard. It is a reliable, consistent, internal layer that surfaces cross-channel marketing performance in one place, on demand.

---

## 2. Business Context

A marketing technology company manages campaigns across multiple D2C client brands simultaneously. The internal team — analysts, account managers, campaign strategists — is responsible for monitoring performance, identifying issues early, and advising clients on where to focus next.

Today, answering a performance question requires someone to log into Meta Ads, GA4, Shopify, and email tools separately, manually compare figures across sources, and write a summary narrative — often in a spreadsheet or slide. This process is slow, inconsistent, and entirely person-dependent. If the person who usually does it is unavailable, the question just sits there unanswered.

---

## 3. Core Problem

**Fragmented reporting workflows create operational bottlenecks.**

The team does not lack data. They have too much of it, spread across too many tools, with no unified view. Every performance check is a manual assembly job. The answer looks different depending on who does it and when — which means the team can't respond to performance drops quickly, and client communication gets delayed.

---

## 4. Primary Users

**Internal team only — v1 is not client-facing.**

| Role | How They Use Orbit |
|---|---|
| Marketing Analyst | Daily performance checks, anomaly identification |
| Account Manager | Pre-client-call briefing, weekly summaries |
| Campaign Strategist | Channel comparison, budget reallocation signals |

### Why not clients?

Making clients the primary user changes the product entirely — it immediately requires authentication layers, role-based access, white-labeling, and polished export flows. That's a different product, and not one v1 should try to be. For v1, the problem being solved is internal workflow fragmentation. Clients benefit downstream when the internal team can answer their questions faster and more consistently.

---

## 5. Product Goals

Orbit v1 optimizes for four things:

1. **Speed** — Performance questions answered in minutes, not hours  
2. **Consistency** — Same numbers, same definitions, same format every time  
3. **Visibility** — Cross-channel view without switching between tools  
4. **Trust** — Every number is traceable to a source, timestamp, and definition  

---

## 6. V1 Feature Set

These are the only features in v1. Scope is intentionally tight.

### Cross-channel performance dashboard

A single view showing key metrics across paid (Meta Ads), web analytics (GA4), and e-commerce (Shopify) for a selected brand and date range. No tool-switching required.

### Core metric display

ROAS, CAC, total spend, conversions, conversion rate, and channel-level traffic — displayed consistently with agreed-upon definitions across all brands.

### Weekly performance summary

An auto-generated text summary of the week's performance — what moved, what didn't, what needs attention. Deterministic, not AI-generated. Based on threshold logic and metric comparisons.

### Anomaly alerts

Simple threshold-based flags: ROAS drops below a defined value, spend exceeds budget by a set percentage, conversion rate changes significantly week-over-week. Visible on the dashboard in v1; push notifications are a future consideration.

### Source transparency layer

Every metric shows its data source, last sync timestamp, and a tooltip with the metric definition. This is non-negotiable for internal trust.

### Brand selector

Switch between client brands within the same interface. Each brand has its own data connection and metric thresholds.

---

## 7. Explicitly Out of Scope — v1

These are deliberate exclusions, not oversights.

| Feature | Why Excluded |
|---|---|
| Predictive AI / forecasting | Adds model complexity and trust risk before baseline reporting is stable |
| Budget automation | Wrong call here has real cost consequences; requires deeper client context |
| AI chatbot assistant | Premature before the reporting layer is reliable |
| Real-time streaming | Daily scheduled ingestion is sufficient for the reporting cadence |
| Client-facing access | Different product entirely; requires auth, white-labeling, access controls |
| Custom report builder | Adds UI complexity; v1 should deliver opinionated, consistent views |
| Push notifications | Nice-to-have; in-dashboard alerts are sufficient for v1 |

The principle: if a feature doesn't directly solve *"making the performance question answerable faster and more consistently,"* it doesn't belong in v1.

---

## 8. Data Sources & Integration Strategy

**Constraint respected:** The team is not changing their existing tools. Orbit reads from existing platforms via API — it does not replace them.

| Platform | Data Type | Integration Method |
|---|---|---|
| Meta Ads | Spend, impressions, ROAS, conversions | Meta Marketing API |
| Google Analytics 4 | Sessions, traffic sources, conversion events | GA4 Data API |
| Shopify | Orders, revenue, conversion rate | Shopify Admin API |
| Email (e.g. Klaviyo) | Open rate, click rate, attributed revenue | Klaviyo API |

### Ingestion approach

Scheduled pulls, not real-time. Data refreshes overnight and on-demand when a user triggers a manual sync — sufficient for daily and weekly reporting cadence.

### Schema standardization

Each platform defines the same metrics differently (Meta and GA4 count conversions differently, for example). Orbit stores all incoming data against a centralized internal schema, applying agreed-upon metric definitions at ingestion so that cross-platform comparisons remain consistent regardless of source-specific variations.

Consistency is enforced at the data layer before metrics ever reach the dashboard.

---

## 9. Trust & Transparency Design

Internal users will only rely on Orbit if they trust what it shows them. Trust is built through transparency, not polish.

Every metric in Orbit includes:

- **Source label** — "from Meta Ads" / "from GA4"  
- **Last synced timestamp** — "last updated 6 hours ago"  
- **Metric definition tooltip** — exactly how the number is calculated and what it includes or excludes  

The weekly summary explicitly states which thresholds triggered each observation — no black-box outputs. If data is missing or a sync failed, Orbit shows a clear error state rather than silently displaying stale data.

### Why this matters

An analyst presenting numbers in a client meeting needs to answer *"where does that number come from?"* in real time. Orbit makes that possible without going back to the source platform.

---

## 10. Before vs. After Workflow

### Before Orbit — Preparing for a weekly client review

```text
Monday morning
↓
Open Meta Ads → export last week's spend and ROAS
↓
Open GA4 → manually note sessions, traffic sources, conversion events
↓
Open Shopify → check revenue and order volume
↓
Open email platform → pull open rate and attributed revenue
↓
Open spreadsheet → paste all numbers in, align date ranges manually
↓
Realise Meta and GA4 conversion numbers don't match → investigate discrepancy
↓
Write performance summary in slides or email
↓
Total time: 1.5 – 3 hours per brand, per week
```

### After Orbit — Same task

```text
Monday morning
↓
Open Orbit → select brand + date range
↓
View unified cross-channel dashboard with all key metrics
↓
Check anomaly flags — one alert: ROAS dropped 18% vs prior week on paid
↓
Read auto-generated weekly summary
↓
Investigate the flagged drop using channel drilldown
↓
Walk into client call with full context
↓
Total time: significantly reduced — from hours to under 30 minutes
```

---

## 11. Assumptions & Tradeoffs

### Assumptions made without full information

- The team uses Meta Ads, GA4, and Shopify as primary tools. Not confirmed — chosen as the most common D2C stack. I also assumed Meta is the primary paid channel, since that's the default for most D2C brands operating in India at this scale.
- API access to existing platforms is available. In practice this requires credential setup — treated as a configuration step, not a blocker.
- Daily scheduled ingestion is sufficient. If intraday reporting is needed, cadence would need to change.

### Tradeoffs made deliberately

- **Opinionated views over custom reports** — Everyone gets the same view. This trades flexibility for consistency, which is the core problem being solved.
- **No AI in v1** — AI-generated summaries feel compelling but introduce trust risk before baseline reporting is established. Deterministic summaries are less impressive but more reliable.
- **Internal-only access** — Keeps scope manageable and lets the tool be validated internally before any client-facing complexity is introduced.

---

## 12. Future Considerations

These are not v1 features. They are worth building toward.

- **Client-facing view** — Read-only, white-labeled access for clients. Requires authentication and access control layer.
- **Forecasting** — Meaningful once 6+ months of clean historical data exists in Orbit.
- **Push alerts** — Slack or email notifications when anomalies are detected.
- **Custom metric definitions per brand** — Some clients define ROAS or conversions differently; v2 could support brand-level configuration.
- **Expanded channel coverage** — LinkedIn Ads, TikTok, YouTube, SEO via Search Console.

---

*Orbit v1 scope — May 2026*
