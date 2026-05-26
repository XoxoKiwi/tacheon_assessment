# Task 1 — Product Scoping: Orbit

## What I Built

A product brief for **Orbit** — an internal marketing performance insights tool designed for a marketing technology company managing multiple D2C client brands.

The core question Orbit answers:

> *"How is our marketing performing across channels right now, and where should we be focusing?"*

---

## Files in This Folder

| File | What It Contains |
|---|---|
| `notes.md` | Initial Day 1 thinking, problem framing, and early scoping questions |
| `product_brief.md` | Full product brief — users, problem, v1 scope, integrations, tradeoffs, and future considerations |
| `user_scenario.md` | A realistic analyst workflow showing how Orbit changes day-to-day reporting operations |
| `walkthrough.md` | A written walkthrough of my thinking process, decisions, tradeoffs, and assumptions |

---

## Key Decisions I Made

### 1. Internal-only for v1

The initial temptation was to make Orbit client-facing as well. I ruled that out quickly because client access immediately introduces authentication, role-based permissions, white-labeling, export flows, and access-control concerns.

That becomes a different product entirely.

Orbit v1 focuses only on solving the internal workflow fragmentation problem first.

---

### 2. No AI in v1

AI-generated summaries sound compelling, but they introduce trust risk before the reporting layer is even reliable.

If analysts cannot clearly verify where a number came from, they are unlikely to trust the system during client discussions.

For v1, I deliberately chose deterministic, threshold-based summaries over AI-generated insights because reliability matters more than sophistication at this stage.

---

### 3. Opinionated views over flexibility

I intentionally excluded a custom report builder.

The core problem Orbit solves is inconsistency — different people manually pulling different versions of the same answer.

A fixed, opinionated reporting layer enforces consistency across teams and brands. Adding too much flexibility too early would weaken that goal.

---

### 4. Schema standardization at ingestion, not the UI layer

Platforms like Meta Ads and GA4 define conversions differently.

Rather than handling this inconsistency in the dashboard itself, I placed normalization logic at ingestion using a centralized internal schema.

This ensures metrics are standardized before they ever reach the reporting layer.

---

## What I Would Revisit With More Time

- **Validate the assumed tool stack** — I assumed Meta Ads, GA4, and Shopify because they are commonly used by D2C brands, especially in the Indian market. In practice, I would confirm the actual stack with the team before designing integrations.
- **Define anomaly thresholds collaboratively** — Placeholder thresholds like *"ROAS dropped 18%"* would need calibration with analysts who understand normal performance patterns for each brand.
- **Prototype the brand selector UX** — Switching between multiple client brands introduces subtle UX problems like filter persistence, context switching, and per-brand preferences.
- **Explore a lightweight client-read view for v2** — Not part of v1, but worth considering early so future authentication and permission layers are not bolted on later.

---

## What I Deliberately Left Out of v1

See **Section 7** of `product_brief.md` for the complete out-of-scope feature table and reasoning.

Features intentionally excluded from v1 include:

- Predictive forecasting
- AI chat assistants
- Budget automation
- Real-time streaming
- Client-facing access
- Custom report builders
- Push notifications

These were excluded because they either:
- introduce trust risk,
- add complexity before the core workflow is stable,
- or solve a different problem entirely.


