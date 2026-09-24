# Data documentation

## Included data

All records in this folder are synthetic.

- `trajectories.json` contains six synthetic employee trajectories with one pre-training baseline and 30/60/90-day follow-ups.
- `sample.csv` is a compact tabular excerpt showing the same schema.

No employee or training-participant data are included.

## What the dataset separates

The schema intentionally keeps three different concepts apart.

### 1. Workplace application evidence

The current baseline can combine four evidence sources:

- self report
- manager observation
- behavior evidence
- objective workplace-application evidence

Each evidence record can also carry a confidence value.

These signals feed the **application score**.

### 2. Transfer conditions

Follow-up records separately store:

- opportunity to perform
- manager support
- tool access
- peer support
- workflow support

These values do **not** multiply the application score.

They are contextual diagnostics that may help explain why transfer is difficult or easy.

### 3. Business/performance outcome

`performance_outcome` is stored separately from workplace application evidence.

This allows the analysis to represent cases where:

- transfer improves but business outcomes remain flat
- business outcomes improve for reasons that may not be training
- transfer and performance move together

The repository does not treat association between these variables as proof that training caused the performance result.

## Longitudinal structure

Every trajectory requires:

- exactly one `baseline` observation with `days_after=0`
- at least one `followup`
- unique positive follow-up days

The bundled dataset uses 30, 60, and 90 days.

Observed persistence is calculated from repeated follow-up scores.

It is **not** created by automatically decaying an earlier score.

## Synthetic cases

The dataset deliberately includes different patterns:

- E01: strong transfer with supportive conditions
- E02: strong application despite limited opportunity to perform
- E03: strong early transfer followed by decline
- E04: substantial disagreement between evidence sources
- E05: limited tool access with maintained application
- E06: improved transfer while the synthetic business outcome remains flat

These cases exist to test software behavior, not to model real employees.

## Evidence provenance

A real adapter should record more than the numeric value.

Useful provenance fields include:

- evidence source
- instrument or rubric
- observation date
- assessor
- task or workflow observed
- evidence confidence
- inter-rater or scoring reliability where applicable
- missingness
- changes to role/task conditions

## Transfer conditions

The five bundled contextual dimensions are a compact prototype, not a validated transfer-climate instrument.

If a real study uses a validated scale such as the Learning Transfer System Inventory or another instrument, preserve that instrument's constructs, scoring rules, licensing, and interpretation rather than mapping it casually into these five values.

## Business outcomes

A real business or performance outcome needs its own definition, measurement window, source, and confound analysis.

Examples could include quality, cycle time, error rate, customer outcome, or another role-relevant metric.

Do not assume a post-training change was caused by training without an appropriate causal design.

## Do not commit

Do not commit identifiable employee records, manager comments, private performance evaluations, compensation information, disciplinary data, health/disability data, raw work products, confidential business KPIs, or proprietary assessment instruments that cannot legally be redistributed.

## Dataset card before real use

Document the intervention, target competency, population, baseline timing, follow-up windows, evidence instruments, condition measures, performance-outcome definitions, missingness, attrition, privacy controls, consent or other lawful basis, known biases, and permitted uses.
