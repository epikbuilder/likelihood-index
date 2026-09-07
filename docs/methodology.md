# Methodology

## Purpose

The Likelihood Index is a directional brand-measurement framework.

It is designed to answer:

> Are the leading indicators of future choice strengthening or weakening, and how much confidence should we place in that conclusion?

It is deliberately not framed as a literal probability that a specific person will purchase.

## Step 1 — Standardize inputs

For metric value `x` with baseline mean `μ` and standard deviation `σ`:

```text
z = (x - μ) / σ
```

The baseline may be:
- the brand's own trailing history,
- a category benchmark,
- a competitive benchmark, or
- another validated norm.

## Step 2 — Bound extreme observations

```text
bounded_effect = tanh(z / 2)
```

This reduces the chance that one unusual metric dominates the system.

## Step 3 — Estimate metric confidence

Each source can receive a confidence multiplier from 0–1 based on:
- recency,
- sample sufficiency,
- source quality,
- coverage,
- data stability,
- and independence from other signals.

## Step 4 — Aggregate within signal families

Metrics are first combined inside their signal family.

This is important. Without domain-first aggregation, the family with the greatest number of available metrics can dominate merely because it has more columns.

## Step 5 — Calculate the Likelihood Index

The default reference formula is:

```text
LI = 50 + 38 × weighted domain effect
```

The index is bounded to 0–100.

A value of 50 represents a neutral directional state, not a 50% chance of purchase.

## Step 6 — Calculate Evidence Confidence

Evidence Confidence is a weighted measure of source confidence and coverage.

Missing data must reduce confidence rather than being silently treated as equivalent evidence.

## Step 7 — Calculate System Coherence

System Coherence captures disagreement between signal families.

Examples:

High coherence:
- share of search rising,
- consideration rising,
- reviews improving,
- creator sentiment improving,
- availability stable or rising.

Low coherence:
- media resonance surging,
- reviews declining,
- availability deteriorating,
- search flat.

A low-coherence system should trigger diagnosis, not celebration.

## Step 8 — Validate against future outcomes

Do not include the outcome being predicted inside the predictor.

Compare the index at time `t` with outcomes at future horizons, for example:
- sales at `t + 4 to 12 weeks`,
- market share,
- penetration,
- new-customer rate,
- consideration,
- purchase intent.

Recommended validation metrics:
- directional hit rate,
- Spearman rank correlation,
- calibration slope,
- lift by index band,
- out-of-sample error.

Only optimize weights after enough historical observations exist.
