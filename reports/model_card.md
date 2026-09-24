# Analytic system card

## System

Training Transfer Analytics

## Purpose

Workplace transfer scoring baseline with evidence weighting, retention decay, and contextual barrier flags.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces a transfer index, a retention adjusted score, and contextual barrier flags. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Use repeated post training measures and independent workplace evidence. Report agreement among evidence sources, sensitivity to weighting, and whether the score predicts meaningful behavior beyond course completion.

## Main limitation

The index is a transparent scoring rule, not a validated transfer measure. Self and manager ratings can be biased, and decay should not be assumed without longitudinal evidence.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
