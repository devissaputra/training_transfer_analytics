# Calculation guide

## Question and evidence

Does observed workplace application persist after training?

Synthetic baseline and follow-up trajectories with self, manager, behavior and objective evidence.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Weight evidence within sources; combine available sources; separate application, conditions and business outcomes.

## Calculation and interpretation

`Persistence ratio = final follow-up application / first follow-up application.`

Missing sources cause active weights to be renormalized. Ratios are undefined when the first follow-up is zero and can exceed one. Before/after change does not establish a training effect without a credible counterfactual.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| final/first follow-up: .6/.8 | 0.7499999999999999 | unitless | `outputs.final/first follow-up: .6/.8` |
| change from baseline: .6-.3 | 0.3 | unitless | `outputs.change from baseline: .6-.3` |
| 30-day change: (.6-.8)/60×30 | -0.10000000000000003 | unitless | `outputs.30-day change: (.6-.8)/60×30` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This longitudinal prototype separates workplace application from transfer conditions and business outcomes. It combines multiple evidence sources with explicit weights, tracks baseline and follow-up changes, and reports disagreement and weight sensitivity instead of hiding them in a single score. The bundled trajectories are synthetic, and observed persistence is described without claiming that training caused the change.

## Verification performed in this review

31 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`validate_evidence_weights`](src/training_transfer_analytics/core.py#L51) | Inspect the explicit implementation and its callers. |
| [`validate_evidence_records`](src/training_transfer_analytics/core.py#L79) | Inspect the explicit implementation and its callers. |
| [`aggregate_transfer_evidence`](src/training_transfer_analytics/core.py#L132) | Aggregate multi-source workplace-application evidence. |
| [`validate_conditions`](src/training_transfer_analytics/core.py#L222) | Inspect the explicit implementation and its callers. |
| [`condition_diagnostics`](src/training_transfer_analytics/core.py#L243) | Describe transfer-climate barriers separately from transfer outcomes. |
| [`validate_trajectory`](src/training_transfer_analytics/core.py#L341) | Inspect the explicit implementation and its callers. |
| [`analyze_trajectory`](src/training_transfer_analytics/core.py#L387) | Analyze baseline change and observed transfer persistence over time. |
| [`cohort_summary`](src/training_transfer_analytics/core.py#L495) | Summarize already-analyzed individual transfer trajectories. |
| [`weight_sensitivity`](src/training_transfer_analytics/core.py#L579) | Re-run one trajectory under alternative evidence-weight assumptions. |
| [`simulate_hypothetical_decay`](src/training_transfer_analytics/core.py#L637) | Simulate assumed exponential decay; this is not observed persistence. |
| [`transfer_index`](src/training_transfer_analytics/core.py#L655) | Backward-compatible three-source application score. |
| [`retention_adjusted`](src/training_transfer_analytics/core.py#L698) | Backward-compatible hypothetical decay simulator. |
| [`barrier_flags`](src/training_transfer_analytics/core.py#L710) | Backward-compatible three-condition barrier labels. |

## What remains before a stronger research claim

Missing sources cause active weights to be renormalized. Ratios are undefined when the first follow-up is zero and can exceed one. Before/after change does not establish a training effect without a credible counterfactual. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
