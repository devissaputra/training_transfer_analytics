# Ethics, safety, and misuse risks

## Intended use

Training Transfer Analytics is a research prototype for examining whether trained behavior appears and persists in workplace evidence.

It is not a performance-management engine, employee-ranking system, promotion score, disciplinary tool, or proof that a training program caused a business result.

## Transfer is not employee worth

A lower transfer score may reflect:

- limited opportunity to use the skill
- weak manager support
- missing tools
- workflow constraints
- peer or team barriers
- a poor match between training and job tasks
- measurement error

Do not interpret low transfer as low intelligence, motivation, commitment, or potential.

## Conditions must stay visible

The prototype deliberately separates application evidence from transfer conditions.

Do not reintroduce a design that silently penalizes an employee's transfer score because the organization failed to provide opportunity, tools, support, or usable workflows.

Those factors are partly organizational responsibilities.

## Manager ratings

Manager ratings may be affected by:

- limited observation
- halo effects
- recency effects
- relationship quality
- inconsistent standards
- bias

They should not automatically be treated as ground truth.

Source disagreement should be reviewed rather than averaged away without inspection.

## Self reports

Self reports can provide useful information about confidence and application, but they can also be affected by memory, social desirability, and differing interpretation of rating scales.

Do not dismiss them automatically, and do not treat them as objective performance evidence.

## Objective evidence

"Objective" evidence still requires scrutiny.

A count, KPI, or system trace may measure opportunity, workload, tool use, or process compliance rather than correct transfer of the trained skill.

Document what the measure actually represents.

## Business performance

Business outcomes are influenced by many factors beyond training.

Do not attribute revenue, quality, cycle time, error-rate, or customer changes to training without an appropriate design.

This repository keeps performance outcomes separate from transfer application for that reason.

## Longitudinal surveillance

Repeated workplace measurement can become surveillance.

Collect the minimum evidence necessary for the research question.

Avoid continuous monitoring simply because it is technically possible.

Prefer defined observation windows and clear retention rules.

## Employment decisions

Do not use this prototype alone for:

- hiring or rejection
- promotion
- termination
- pay
- discipline
- forced ranking
- performance ratings
- succession decisions

If training-transfer evidence is visible to managers, clearly define whether and how it may be used.

A development study should not quietly become an employment-scoring system.

## Privacy

Workplace transfer datasets may contain:

- performance records
- manager judgments
- work-system traces
- customer outcomes
- project history
- learning history

These can be sensitive even when direct identifiers are removed.

Define access, retention, correction, deletion, and purpose-limitation rules.

## Opportunity-to-perform fairness

Employees do not receive equal access to:

- assignments
- tools
- customers
- systems
- manager attention
- mentoring
- project responsibility

A lack of demonstrated transfer may therefore reflect unequal opportunity.

Review access conditions before drawing conclusions about individuals or groups.

## Thresholds

The prototype's barrier threshold is a review heuristic.

Do not present a value below 0.5 as a validated diagnosis of poor support unless the underlying instrument and cutoff have been validated for that use.

## Before real deployment

Document the intervention, measurement instruments, workplace evidence sources, rating process, transfer conditions, privacy rules, employee visibility, correction process, attrition, source disagreement handling, role of managers, allowed downstream uses, and a clear boundary preventing developmental analytics from becoming automated employment decisions.
