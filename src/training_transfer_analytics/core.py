import math
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from numbers import Real
from statistics import mean, pstdev


EVIDENCE_SOURCES = (
    "self",
    "manager",
    "behavior",
    "objective",
)

DEFAULT_EVIDENCE_WEIGHTS = {
    "self": 0.15,
    "manager": 0.20,
    "behavior": 0.30,
    "objective": 0.35,
}

CONDITION_FIELDS = (
    "opportunity_to_perform",
    "manager_support",
    "tool_access",
    "peer_support",
    "workflow_support",
)


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _unit_interval(value, name):
    value = _finite_number(value, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def validate_evidence_weights(weights=None):
    weights = dict(
        DEFAULT_EVIDENCE_WEIGHTS
        if weights is None
        else weights
    )
    if set(weights) != set(EVIDENCE_SOURCES):
        raise ValueError(
            f"weights must contain exactly {list(EVIDENCE_SOURCES)}"
        )

    normalized = {}
    for source, value in weights.items():
        value = _finite_number(value, f"{source} weight")
        if value < 0:
            raise ValueError("evidence weights must be non-negative")
        normalized[source] = value

    total = sum(normalized.values())
    if total <= 0:
        raise ValueError("at least one evidence weight must be positive")

    return {
        source: value / total
        for source, value in normalized.items()
    }


def validate_evidence_records(records):
    if (
        not isinstance(records, Sequence)
        or isinstance(records, (str, bytes))
        or not records
    ):
        raise ValueError("evidence records must be a non-empty sequence")

    normalized = []
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ValueError("each evidence record must be a mapping")

        source = record.get("source")
        if source not in EVIDENCE_SOURCES:
            raise ValueError(
                f"record {index} has unknown evidence source: {source}"
            )

        value = _unit_interval(
            record.get("value"),
            f"record {index} value",
        )
        confidence = _unit_interval(
            record.get("confidence", 1.0),
            f"record {index} confidence",
        )

        instrument = record.get("instrument")
        if instrument is not None and (
            not isinstance(instrument, str)
            or not instrument.strip()
        ):
            raise ValueError(
                "instrument must be a non-empty string when supplied"
            )

        normalized.append(
            {
                "source": source,
                "value": value,
                "confidence": confidence,
                "instrument": (
                    instrument.strip()
                    if instrument
                    else None
                ),
            }
        )

    return normalized


def aggregate_transfer_evidence(
    records,
    *,
    weights=None,
    disagreement_threshold=0.25,
):
    """Aggregate multi-source workplace-application evidence.

    Transfer conditions such as opportunity or manager support are intentionally
    not included in this outcome score.
    """
    weights = validate_evidence_weights(weights)
    records = validate_evidence_records(records)
    disagreement_threshold = _unit_interval(
        disagreement_threshold,
        "disagreement_threshold",
    )

    grouped = defaultdict(list)
    for record in records:
        grouped[record["source"]].append(record)

    source_scores = {}
    source_confidence = {}
    for source, source_records in grouped.items():
        total_confidence = sum(
            record["confidence"]
            for record in source_records
        )
        if total_confidence <= 0:
            source_scores[source] = None
            source_confidence[source] = 0.0
            continue

        source_scores[source] = sum(
            record["value"] * record["confidence"]
            for record in source_records
        ) / total_confidence
        source_confidence[source] = (
            total_confidence / len(source_records)
        )

    active = [
        source
        for source in EVIDENCE_SOURCES
        if source_scores.get(source) is not None
        and weights[source] > 0
    ]
    if not active:
        raise ValueError(
            "no positive-confidence evidence is available "
            "for sources with positive weight"
        )

    active_weight = sum(weights[source] for source in active)
    normalized_active_weights = {
        source: weights[source] / active_weight
        for source in active
    }

    application_score = sum(
        source_scores[source]
        * normalized_active_weights[source]
        for source in active
    )

    values = [source_scores[source] for source in active]
    agreement_range = max(values) - min(values)
    agreement_sd = pstdev(values) if len(values) > 1 else 0.0

    return {
        "application_score": application_score,
        "source_scores": {
            source: source_scores.get(source)
            for source in EVIDENCE_SOURCES
        },
        "source_confidence": {
            source: source_confidence.get(source)
            for source in EVIDENCE_SOURCES
        },
        "active_weights": normalized_active_weights,
        "source_coverage": len(active) / len(EVIDENCE_SOURCES),
        "agreement_range": agreement_range,
        "agreement_sd": agreement_sd,
        "disagreement_flag": (
            agreement_range > disagreement_threshold
        ),
    }


def validate_conditions(conditions):
    if not isinstance(conditions, Mapping):
        raise ValueError("conditions must be a mapping")

    missing = set(CONDITION_FIELDS) - set(conditions)
    unknown = set(conditions) - set(CONDITION_FIELDS)
    if missing or unknown:
        raise ValueError(
            "conditions must contain exactly "
            f"{list(CONDITION_FIELDS)}"
        )

    return {
        field: _unit_interval(
            conditions[field],
            field,
        )
        for field in CONDITION_FIELDS
    }


def condition_diagnostics(
    conditions,
    *,
    review_threshold=0.5,
):
    """Describe transfer-climate barriers separately from transfer outcomes."""
    conditions = validate_conditions(conditions)
    review_threshold = _unit_interval(
        review_threshold,
        "review_threshold",
    )

    barriers = []
    for field, value in conditions.items():
        severity = max(0.0, review_threshold - value)
        if severity > 0:
            barriers.append(
                {
                    "condition": field,
                    "value": value,
                    "severity": severity,
                }
            )

    barriers.sort(
        key=lambda row: (
            -row["severity"],
            row["condition"],
        )
    )

    return {
        "conditions": conditions,
        "review_threshold": review_threshold,
        "barriers": barriers,
        "barrier_count": len(barriers),
        "minimum_condition": min(conditions.values()),
        "mean_condition": mean(conditions.values()),
    }


def _validate_timepoint(observation, index):
    if not isinstance(observation, Mapping):
        raise ValueError("each observation must be a mapping")

    phase = observation.get("phase")
    if phase not in {"baseline", "followup"}:
        raise ValueError(
            f"observation {index} phase must be baseline or followup"
        )

    days_after = observation.get("days_after")
    if (
        isinstance(days_after, bool)
        or not isinstance(days_after, int)
        or days_after < 0
    ):
        raise ValueError(
            f"observation {index} days_after must be "
            "a non-negative integer"
        )

    if phase == "baseline" and days_after != 0:
        raise ValueError("baseline observation must use days_after=0")
    if phase == "followup" and days_after <= 0:
        raise ValueError("followup days_after must be positive")

    evidence = validate_evidence_records(
        observation.get("evidence")
    )

    performance_outcome = observation.get("performance_outcome")
    if performance_outcome is not None:
        performance_outcome = _unit_interval(
            performance_outcome,
            f"observation {index} performance_outcome",
        )

    conditions = observation.get("conditions")
    if phase == "baseline":
        if conditions is not None:
            conditions = validate_conditions(conditions)
    else:
        if conditions is None:
            raise ValueError(
                "followup observations must include transfer conditions"
            )
        conditions = validate_conditions(conditions)

    return {
        "phase": phase,
        "days_after": days_after,
        "evidence": evidence,
        "conditions": conditions,
        "performance_outcome": performance_outcome,
    }


def validate_trajectory(observations):
    if (
        not isinstance(observations, Sequence)
        or isinstance(observations, (str, bytes))
        or len(observations) < 2
    ):
        raise ValueError(
            "trajectory must contain one baseline "
            "and at least one followup"
        )

    normalized = [
        _validate_timepoint(observation, index)
        for index, observation in enumerate(observations)
    ]

    baseline = [
        row for row in normalized
        if row["phase"] == "baseline"
    ]
    followups = [
        row for row in normalized
        if row["phase"] == "followup"
    ]

    if len(baseline) != 1:
        raise ValueError(
            "trajectory must contain exactly one baseline"
        )
    if not followups:
        raise ValueError(
            "trajectory must contain at least one followup"
        )

    days = [row["days_after"] for row in followups]
    if len(days) != len(set(days)):
        raise ValueError(
            "followup days_after values must be unique"
        )

    return [baseline[0]] + sorted(
        followups,
        key=lambda row: row["days_after"],
    )


def analyze_trajectory(
    observations,
    *,
    weights=None,
    disagreement_threshold=0.25,
    barrier_threshold=0.5,
):
    """Analyze baseline change and observed transfer persistence over time."""
    observations = validate_trajectory(observations)

    analyzed = []
    for observation in observations:
        evidence = aggregate_transfer_evidence(
            observation["evidence"],
            weights=weights,
            disagreement_threshold=disagreement_threshold,
        )
        condition_review = (
            None
            if observation["conditions"] is None
            else condition_diagnostics(
                observation["conditions"],
                review_threshold=barrier_threshold,
            )
        )
        analyzed.append(
            {
                "phase": observation["phase"],
                "days_after": observation["days_after"],
                "application_score": evidence["application_score"],
                "source_scores": evidence["source_scores"],
                "source_coverage": evidence["source_coverage"],
                "agreement_range": evidence["agreement_range"],
                "agreement_sd": evidence["agreement_sd"],
                "disagreement_flag": evidence["disagreement_flag"],
                "condition_review": condition_review,
                "performance_outcome": observation["performance_outcome"],
            }
        )

    baseline = analyzed[0]
    followups = analyzed[1:]

    for row in followups:
        row["change_from_baseline"] = (
            row["application_score"]
            - baseline["application_score"]
        )

    first = followups[0]
    final = followups[-1]

    observed_persistence_ratio = (
        final["application_score"]
        / first["application_score"]
        if first["application_score"] > 0
        else None
    )

    followup_change = (
        final["application_score"]
        - first["application_score"]
    )

    if len(followups) > 1:
        day_span = (
            final["days_after"]
            - first["days_after"]
        )
        change_per_30_days = (
            followup_change / day_span * 30
            if day_span > 0
            else None
        )
    else:
        change_per_30_days = None

    baseline_performance = baseline["performance_outcome"]
    final_performance = final["performance_outcome"]
    performance_change = (
        final_performance - baseline_performance
        if (
            baseline_performance is not None
            and final_performance is not None
        )
        else None
    )

    return {
        "baseline_score": baseline["application_score"],
        "first_followup_score": first["application_score"],
        "final_followup_score": final["application_score"],
        "first_change_from_baseline": first["change_from_baseline"],
        "final_change_from_baseline": final["change_from_baseline"],
        "observed_persistence_ratio": observed_persistence_ratio,
        "followup_change": followup_change,
        "change_per_30_days": change_per_30_days,
        "baseline_performance_outcome": baseline_performance,
        "final_performance_outcome": final_performance,
        "performance_outcome_change": performance_change,
        "disagreement_timepoints": sum(
            1 for row in analyzed
            if row["disagreement_flag"]
        ),
        "timepoints": analyzed,
    }


def cohort_summary(trajectories):
    """Summarize already-analyzed individual transfer trajectories."""
    if (
        not isinstance(trajectories, Sequence)
        or isinstance(trajectories, (str, bytes))
        or not trajectories
    ):
        raise ValueError(
            "trajectories must be a non-empty sequence"
        )

    required = {
        "baseline_score",
        "first_followup_score",
        "final_followup_score",
        "final_change_from_baseline",
        "observed_persistence_ratio",
        "timepoints",
        "performance_outcome_change",
    }
    for trajectory in trajectories:
        if (
            not isinstance(trajectory, Mapping)
            or not required.issubset(trajectory)
        ):
            raise ValueError(
                "each trajectory must be an analyze_trajectory output"
            )

    persistence_values = [
        trajectory["observed_persistence_ratio"]
        for trajectory in trajectories
        if trajectory["observed_persistence_ratio"] is not None
    ]

    performance_changes = [
        trajectory["performance_outcome_change"]
        for trajectory in trajectories
        if trajectory["performance_outcome_change"] is not None
    ]

    barrier_counts = Counter()
    for trajectory in trajectories:
        for timepoint in trajectory["timepoints"]:
            review = timepoint["condition_review"]
            if review is None:
                continue
            for barrier in review["barriers"]:
                barrier_counts[barrier["condition"]] += 1

    return {
        "n": len(trajectories),
        "mean_baseline_score": mean(
            trajectory["baseline_score"]
            for trajectory in trajectories
        ),
        "mean_first_followup_score": mean(
            trajectory["first_followup_score"]
            for trajectory in trajectories
        ),
        "mean_final_followup_score": mean(
            trajectory["final_followup_score"]
            for trajectory in trajectories
        ),
        "mean_final_change_from_baseline": mean(
            trajectory["final_change_from_baseline"]
            for trajectory in trajectories
        ),
        "mean_observed_persistence_ratio": (
            mean(persistence_values)
            if persistence_values
            else None
        ),
        "mean_performance_outcome_change": (
            mean(performance_changes)
            if performance_changes
            else None
        ),
        "barrier_counts": dict(
            sorted(barrier_counts.items())
        ),
    }


def weight_sensitivity(
    observations,
    weight_scenarios,
    *,
    disagreement_threshold=0.25,
    barrier_threshold=0.5,
):
    """Re-run one trajectory under alternative evidence-weight assumptions."""
    if (
        not isinstance(weight_scenarios, Mapping)
        or not weight_scenarios
    ):
        raise ValueError(
            "weight_scenarios must be a non-empty mapping"
        )

    scenarios = {}
    for name, weights in weight_scenarios.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "scenario names must be non-empty strings"
            )
        result = analyze_trajectory(
            observations,
            weights=weights,
            disagreement_threshold=disagreement_threshold,
            barrier_threshold=barrier_threshold,
        )
        scenarios[name] = {
            "baseline_score": result["baseline_score"],
            "first_followup_score": result["first_followup_score"],
            "final_followup_score": result["final_followup_score"],
            "final_change_from_baseline": result["final_change_from_baseline"],
            "observed_persistence_ratio": result["observed_persistence_ratio"],
        }

    final_scores = [
        row["final_followup_score"]
        for row in scenarios.values()
    ]
    final_changes = [
        row["final_change_from_baseline"]
        for row in scenarios.values()
    ]

    return {
        "scenarios": scenarios,
        "final_score_range": (
            min(final_scores),
            max(final_scores),
        ),
        "final_change_range": (
            min(final_changes),
            max(final_changes),
        ),
    }


def simulate_hypothetical_decay(
    score,
    days,
    *,
    half_life=60,
):
    """Simulate assumed exponential decay; this is not observed persistence."""
    score = _unit_interval(score, "score")
    if isinstance(days, bool) or not isinstance(days, int):
        raise ValueError("days must be an integer")
    if days < 0:
        raise ValueError("days must be non-negative")
    half_life = _finite_number(half_life, "half_life")
    if half_life <= 0:
        raise ValueError("half_life must be positive")
    return score * (0.5 ** (days / half_life))


def transfer_index(
    self_rating,
    manager_rating,
    behavior_score,
    opportunity=None,
):
    """Backward-compatible three-source application score.

    opportunity is accepted for compatibility and validated when supplied,
    but it intentionally does not alter the transfer outcome.
    """
    records = [
        {
            "source": "self",
            "value": self_rating,
            "confidence": 1.0,
        },
        {
            "source": "manager",
            "value": manager_rating,
            "confidence": 1.0,
        },
        {
            "source": "behavior",
            "value": behavior_score,
            "confidence": 1.0,
        },
    ]
    if opportunity is not None:
        _unit_interval(opportunity, "opportunity")

    weights = {
        "self": 0.25,
        "manager": 0.35,
        "behavior": 0.40,
        "objective": 0.0,
    }
    return aggregate_transfer_evidence(
        records,
        weights=weights,
    )["application_score"]


def retention_adjusted(index, days, half_life=60):
    """Backward-compatible hypothetical decay simulator.

    Do not interpret this as measured transfer persistence.
    """
    return simulate_hypothetical_decay(
        index,
        days,
        half_life=half_life,
    )


def barrier_flags(
    manager_support,
    opportunity,
    tool_access,
):
    """Backward-compatible three-condition barrier labels."""
    review = condition_diagnostics(
        {
            "opportunity_to_perform": opportunity,
            "manager_support": manager_support,
            "tool_access": tool_access,
            "peer_support": 1.0,
            "workflow_support": 1.0,
        }
    )
    return [
        barrier["condition"]
        for barrier in review["barriers"]
    ]
