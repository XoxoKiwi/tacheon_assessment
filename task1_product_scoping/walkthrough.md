# Walkthrough — Task 1: Product Scoping

*A written narrative of my thinking process — what I considered, what I ruled out, and where I had to make calls without full information.*

---

## Where I Started

The brief gave me one recurring question: *"How is our marketing performing across channels right now, and where should we be focusing?"*

My first instinct was to ask: why can't anyone answer this today? The data clearly exists — the team has Meta Ads, GA4, Shopify. The problem isn't missing data. The problem is that answering the question requires someone to manually collect it, stitch it together, and interpret it. Every time. And the answer looks different depending on who does it.

That framing changed how I approached the whole scope. This isn't a data problem. It's a workflow and consistency problem. The tool I'm scoping needs to eliminate the manual assembly — not add more data or more intelligence on top of a broken process.

---

## The First Decision: Who Is This For?

The scenario mentions both internal team members and clients asking the same question. My first instinct was to build for both.

I ruled that out within about five minutes of thinking it through.

Building for clients changes everything. You immediately need login systems, role-based access, white-labeling, polished export flows, and careful decisions about what clients can and can't see. That's a completely different product with a completely different set of risks.

The internal problem is the one causing operational pain right now. Solve that first. Clients benefit downstream when the internal team can answer their questions faster and more consistently.

So: **internal team only, v1.**

---

## The Second Decision: What Does v1 Actually Do?

Once I had the user, I asked: what is the simplest version of this that would genuinely change how they work?

Not the most impressive version. The simplest genuinely useful one.

I landed on four things that v1 must do:
- Show cross-channel metrics in one place (no tool-switching)
- Use consistent definitions across all brands (no more "which number is right?")
- Flag anomalies automatically (so the analyst doesn't have to go looking)
- Show where every number came from (so they can defend it in a client meeting)

Everything else — AI summaries, forecasting, budget automation, custom reports — I asked myself: does this directly solve the workflow fragmentation problem? If the answer was "not really" or "only after the core is stable," it went out of scope.

---

## The Decision I Was Least Sure About: No AI

This was the hardest call.

It's a Data & AI product engineer role. Not including AI anywhere might look like I missed the point.

But here's my reasoning: AI-generated summaries introduce trust risk before the reporting layer is even reliable. If an analyst is presenting numbers to a client and they came from an AI summary they can't fully verify, that's a liability, not a feature. The whole product is built on the premise that people need to *trust* what Orbit shows them.

Deterministic summaries — based on threshold logic, clearly showing what triggered each observation — are less impressive but far more trustworthy at this stage. Once the data layer is stable and the team has built confidence in Orbit's numbers, AI becomes a natural v2 addition.

I'm not against AI in this product. I'm against AI before the foundation is solid.

---

## The Data Layer Thinking

The constraint was clear: the team isn't changing their tools. Orbit reads from existing platforms, it doesn't replace them.

The interesting problem here is metric normalization. Meta and GA4 both report "conversions" — but they measure them differently. If you just pull both numbers and display them side by side, you've recreated the problem Orbit is supposed to solve.

My decision: normalize at ingestion, not at the UI layer. When data comes in from each platform, it gets mapped against a centralized internal schema with agreed-upon definitions. By the time it hits the dashboard, there's one number, one definition, one source of truth.

This is the kind of decision that doesn't show up in a wireframe but completely changes how trustworthy the product feels in practice.

---

## What I Would Do Differently With More Time

**Talk to an analyst first.** Everything I scoped is based on reasoning from the outside. A 30-minute conversation with one person who actually does this workflow every Monday morning would probably change three things I got wrong.

**Prototype the anomaly threshold logic.** Right now "ROAS drops 18% week-over-week" is a placeholder. In practice, thresholds need to be calibrated per brand, per channel, and possibly per season. That's a product design problem worth spending real time on.

**Sketch the brand selector more carefully.** Switching between multiple client brands sounds simple but has real edge cases — what happens to your saved filters when you switch? Does each brand remember your last date range? These are small UX details that matter a lot when someone is using this every day under time pressure.

---

## Final Thought

The best thing I did in this scoping exercise was decide what Orbit is *not*. Every feature I kept out of v1 has a reason. The product is opinionated by design — because the problem being solved is inconsistency, and inconsistency gets worse, not better, when you add optionality.

