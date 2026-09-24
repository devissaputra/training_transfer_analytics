import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from training_transfer_analytics.core import (
    DEFAULT_EVIDENCE_WEIGHTS,
    analyze_trajectory,
    cohort_summary,
    simulate_hypothetical_decay,
    weight_sensitivity,
)


with (ROOT / "data" / "trajectories.json").open(
    encoding="utf-8"
) as handle:
    people = json.load(handle)

analyses = []
print("Training Transfer Analytics synthetic demo")
print()

for person in people:
    result = analyze_trajectory(
        person["observations"],
        weights=DEFAULT_EVIDENCE_WEIGHTS,
    )
    analyses.append(result)

    final = result["timepoints"][-1]
    barriers = [
        row["condition"]
        for row in final["condition_review"]["barriers"]
    ]

    print(
        person["employee"],
        {
            "case": person["case"],
            "baseline": round(result["baseline_score"], 3),
            "day30": round(result["first_followup_score"], 3),
            "final": round(result["final_followup_score"], 3),
            "final_change": round(
                result["final_change_from_baseline"],
                3,
            ),
            "persistence_ratio": round(
                result["observed_persistence_ratio"],
                3,
            ),
            "performance_change": (
                None
                if result["performance_outcome_change"] is None
                else round(
                    result["performance_outcome_change"],
                    3,
                )
            ),
            "disagreement_timepoints": result[
                "disagreement_timepoints"
            ],
            "final_barriers": barriers,
        },
    )

print("\nCohort summary:")
print(cohort_summary(analyses))

sensitivity = weight_sensitivity(
    people[3]["observations"],
    {
        "balanced": DEFAULT_EVIDENCE_WEIGHTS,
        "behavior_heavy": {
            "self": 0.05,
            "manager": 0.10,
            "behavior": 0.55,
            "objective": 0.30,
        },
        "manager_heavy": {
            "self": 0.05,
            "manager": 0.60,
            "behavior": 0.20,
            "objective": 0.15,
        },
        "objective_heavy": {
            "self": 0.05,
            "manager": 0.10,
            "behavior": 0.20,
            "objective": 0.65,
        },
    },
)

print("\nWeight sensitivity for E04:")
for name, values in sensitivity["scenarios"].items():
    print(
        name,
        {
            key: round(value, 3)
            if value is not None
            else None
            for key, value in values.items()
        },
    )

print("\nHypothetical decay example (simulation only):")
print(
    round(
        simulate_hypothetical_decay(
            0.72,
            60,
            half_life=60,
        ),
        3,
    )
)

print(
    "\nNote: all data are synthetic. Observed persistence comes "
    "from repeated follow-up measurements. The decay function above "
    "is shown only as a hypothetical sensitivity tool and is not "
    "used to create the transfer trajectories."
)
