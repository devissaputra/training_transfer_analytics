# Research protocol

## Project

Training Transfer Analytics

## Research questions

1. How much does workplace application change from a pre-training baseline?
2. Is that application maintained across repeated follow-up periods?
3. How much do self, manager, behavior, and objective evidence agree?
4. Which transfer conditions are weak when application is low or declining?
5. How sensitive are conclusions to evidence-weight assumptions?
6. Does workplace application move with a separate business/performance outcome, and where do they diverge?

## Conceptual boundary

The current baseline separates three layers.

### Transfer outcome

Transfer is operationalized as workplace application evidence after training.

The current software can combine:

- self report
- manager observation
- behavior evidence
- objective workplace-application evidence

The resulting application score is a transparent composite.

It is not a validated universal measure of transfer.

### Transfer conditions

The prototype separately records:

- opportunity to perform
- manager support
- tool access
- peer support
- workflow support

These conditions are not multiplied into the transfer outcome.

A person can therefore show strong application under poor conditions, or weak application under good conditions.

That distinction is analytically useful.

### Business/performance outcome

A separate optional performance outcome can be recorded at each time point.

The software does not treat business performance as the same construct as transfer and does not attribute performance change to training.

## Longitudinal design

A valid trajectory requires:

- one baseline before transfer is evaluated
- at least one post-training follow-up
- unique follow-up time points

The synthetic demonstration uses 30, 60, and 90 days.

Observed persistence is calculated from repeated follow-up measurements.

The primary persistence quantities are:

- first post-training application score
- final application score
- final / first follow-up ratio
- change from first to final follow-up
- change per 30 days when repeated follow-ups exist

This is descriptive persistence, not a causal model of forgetting.

## Evidence aggregation

Each evidence record contains:

- source
- value
- confidence
- optional instrument label

Multiple records from the same source are first combined using confidence weighting.

Source-level scores are then combined using explicit source weights.

If some evidence sources are absent, the available source weights are renormalized.

The default source weights are a baseline design choice, not an empirically validated truth.

## Evidence disagreement

The software reports:

- source-level values
- source coverage
- range across active sources
- standard deviation across active sources
- a configurable disagreement flag

A composite score should not hide large disagreement between self, manager, behavior, and objective evidence.

## Transfer-climate diagnostics

Each contextual condition remains visible.

A configurable review threshold produces:

- barrier labels
- barrier values
- barrier severity
- minimum condition
- mean condition

The threshold is a review heuristic.

It is not a validated clinical or employment cutoff.

## Weight sensitivity

`weight_sensitivity()` reruns a trajectory under alternative evidence-weight schemes.

Useful scenarios can include:

- balanced
- behavior-heavy
- manager-heavy
- objective-heavy
- self-report-light

Report the range of final application scores and final baseline changes across scenarios.

If the conclusion changes substantially under plausible weights, the composite should be treated as unstable.

## Cohort summaries

The current cohort summary reports:

- mean baseline application
- mean first follow-up application
- mean final follow-up application
- mean final baseline change
- mean observed persistence ratio
- mean separate performance-outcome change where available
- counts of contextual barriers

These are descriptive aggregates.

They do not estimate training effects.

## Hypothetical decay

The repository retains an exponential half-life function only as an explicitly labeled **simulation tool**.

It is not used to generate the longitudinal application trajectories.

A half-life assumption can be useful for sensitivity exercises, but it must not be presented as measured persistence without longitudinal evidence.

## Empirical validation plan

A serious study should pre-specify:

1. target competency and intervention
2. baseline measurement window
3. post-training follow-up windows
4. evidence instruments
5. outcome scoring rules
6. transfer-condition measures
7. attrition handling
8. missing evidence rules
9. performance-outcome definition
10. analysis plan

### Measurement validity

Test whether each evidence source represents workplace application rather than satisfaction, recall, or course completion.

### Reliability

Where human ratings are used, assess scoring consistency and rater agreement.

### Longitudinal validity

Check whether observed application is maintained, declines, or grows over time using actual repeated measurements.

### Incremental value

Compare transfer evidence with simpler indicators such as training completion or immediate post-test results.

### Condition validity

Use validated transfer-climate instruments where appropriate rather than assuming the five prototype conditions are complete.

### Causal inference

If the research question is whether training **caused** improvement, use a design capable of supporting that inference.

Simple pre/post improvement is not enough because job demands, tools, staffing, management changes, seasonal demand, selection into training, and other factors may also change.

## Threats to validity

Major threats include:

- common-method bias
- manager-rating bias
- self-report inflation or deflation
- changing opportunities to demonstrate the skill
- measurement drift across follow-up periods
- attrition
- changes in job role
- concurrent interventions
- regression to the mean
- selection into training
- arbitrary source weights
- incomplete transfer-climate measurement
- business outcomes that are influenced by many factors unrelated to training

The repository is designed to keep those assumptions visible rather than compress them into one unexplained transfer score.
