# Analytic system card

## System

Training Transfer Analytics

## Purpose

Transparent longitudinal analysis of workplace application evidence after training, with separate transfer-condition diagnostics and optional business-performance outcomes.

## Current maturity

Working research prototype.

All bundled records are synthetic.

The repository does not establish a validated transfer measure and does not estimate the causal effect of training.

## Inputs

### Evidence records

Each workplace-application evidence record contains:

- source
- value from 0 to 1
- confidence from 0 to 1
- optional instrument label

Supported source categories are:

- self
- manager
- behavior
- objective

### Transfer conditions

Follow-up time points contain:

- opportunity to perform
- manager support
- tool access
- peer support
- workflow support

### Performance outcome

A separate optional value can represent a role-relevant business or performance outcome.

It does not enter the transfer application score.

### Time

Each trajectory contains:

- one baseline at day 0
- one or more positive follow-up days

## Evidence aggregation

Multiple records from the same source are confidence-weighted.

Available source scores are then combined using explicit evidence weights.

Missing sources cause the remaining source weights to be renormalized.

The system returns source-level values so the composite remains inspectable.

## Application score

The application score is a transparent composite of available workplace-application evidence.

It does not include opportunity, manager support, tools, peer support, workflow support, or business performance.

## Evidence agreement

The output includes:

- source coverage
- range across active sources
- standard deviation across active sources
- disagreement flag

A high composite should not hide major disagreement between evidence sources.

## Longitudinal outputs

For each trajectory the system reports:

- baseline application
- first follow-up application
- final follow-up application
- change from baseline
- observed persistence ratio
- change across the follow-up period
- rate of change per 30 days when possible
- disagreement time points
- contextual barriers at each follow-up
- separate performance-outcome change where available

## Transfer-condition diagnostics

The condition review reports values and threshold-based barrier severity.

The barrier threshold is configurable and is not a validated cutoff.

## Weight sensitivity

The same trajectory can be recomputed under different source-weight assumptions.

This reveals how much the conclusion depends on treating one evidence source as more important than another.

## Cohort outputs

The cohort summary reports descriptive means and barrier counts.

It does not estimate treatment effects.

## Hypothetical decay

A half-life decay function is retained as a simulation utility only.

It is not used to construct observed persistence.

## Main limitations

The current baseline:

- uses a hand-designed composite
- assumes all evidence values are already on a comparable 0–1 scale
- does not validate source instruments
- does not model rater reliability
- does not model missing-not-at-random follow-up
- does not estimate uncertainty intervals
- does not adjust for concurrent workplace changes
- does not estimate causal training effects
- uses a simplified transfer-condition representation

## Evidence needed before real use

A real study needs evidence for:

- construct validity
- scoring reliability
- rater agreement where relevant
- longitudinal measurement consistency
- transfer-condition validity
- attrition handling
- source-weight justification
- sensitivity of conclusions
- separation of transfer from business outcomes
- privacy and employment-use governance

## Human oversight

A reviewer should inspect the source-level evidence, disagreement, transfer conditions, time pattern, and outcome definitions before interpreting a composite.

No output from this prototype should automatically affect employment decisions.
