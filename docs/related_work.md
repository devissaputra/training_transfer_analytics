# Related work and methodological context

Training Transfer Analytics is an original transparent implementation.

It does not reproduce a validated transfer instrument and does not claim that its synthetic scoring rules reproduce published empirical results.

## Transfer as generalization and maintenance

Baldwin and Ford's classic review distinguishes transfer in terms of generalization of learned material to the job and maintenance of trained skills over time.

- Baldwin TT, Ford JK. *Transfer of Training: A Review and Directions for Future Research.* Personnel Psychology. 1988;41(1):63–105.
- https://doi.org/10.1111/j.1744-6570.1988.tb00632.x

That distinction motivates two design choices in this repository:

1. workplace application is measured separately from course completion
2. persistence is based on repeated follow-up observations rather than an assumed decay curve

## Predictors and transfer conditions

Blume, Ford, Baldwin, and Huang meta-analyzed 89 studies and reported relationships between transfer and trainee characteristics, work-environment factors, and training interventions.

- Blume BD, Ford JK, Baldwin TT, Huang JL. *Transfer of Training: A Meta-Analytic Review.* Journal of Management. 2010;36(4):1065–1105.
- https://doi.org/10.1177/0149206309352880

The repository does not use those relationships as causal coefficients.

It instead keeps contextual conditions visible so they can be inspected alongside application evidence.

## Training design, learner, and work environment

Burke and Hutchins reviewed transfer research across HRD, management, adult learning, performance improvement, and psychology, emphasizing learner characteristics, intervention design/delivery, and work-environment influences.

- Burke LA, Hutchins HM. *Training Transfer: An Integrative Literature Review.* Human Resource Development Review. 2007;6(3).
- https://doi.org/10.1177/1534484307303035

The current prototype models only a small subset of workplace conditions and does not claim complete coverage of the transfer system.

## Learning Transfer System Inventory

Holton, Bates, and Ruona developed the generalized Learning Transfer System Inventory (LTSI) to measure multiple factors affecting transfer of learning.

- Holton EF III, Bates RA, Ruona WEA. *Development of a Generalized Learning Transfer System Inventory.* Human Resource Development Quarterly. 2000;11(4):333–360.
- https://doi.org/10.1002/1532-1096(200024)11:4%3C333::AID-HRDQ2%3E3.0.CO;2-P

The five condition fields in this repository are **not** the LTSI and should not be described as such.

A real study that uses the LTSI should preserve its validated constructs, scoring, licensing, and interpretation.

## Why source disagreement matters

Transfer is often measured with different sources and criteria.

A self report, manager judgment, behavior observation, and system-derived measure may disagree because they observe different aspects of application or because one source is biased or noisy.

The current baseline therefore returns source-level scores and disagreement diagnostics rather than exposing only one composite.

## Transfer versus business performance

Applying a trained skill at work is not identical to a business result.

Business outcomes can be influenced by demand, staffing, process design, tools, incentives, customers, and other simultaneous changes.

The current data model keeps an optional performance outcome separate from transfer evidence so the two can be compared without being conflated.

## Scope boundary

Implemented:

- pre-training baseline
- repeated post-training follow-up
- multi-source application evidence
- source confidence
- configurable evidence weights
- source coverage and disagreement
- transfer-condition diagnostics
- observed persistence
- baseline change
- cohort summaries
- separate business/performance outcome
- weight sensitivity
- optional hypothetical decay simulation

Not implemented:

- validated transfer psychometrics
- causal training-effect estimation
- mixed-effects longitudinal models
- latent-variable models
- automated transfer prediction
- validated LTSI scoring
- employment decision automation
