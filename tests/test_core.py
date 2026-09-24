import math
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)
from training_transfer_analytics import core


WEIGHTS = {
    "self": 0.15,
    "manager": 0.20,
    "behavior": 0.30,
    "objective": 0.35,
}

GOOD_CONDITIONS = {
    "opportunity_to_perform": 0.8,
    "manager_support": 0.8,
    "tool_access": 0.9,
    "peer_support": 0.8,
    "workflow_support": 0.85,
}

LOW_OPPORTUNITY = {
    "opportunity_to_perform": 0.3,
    "manager_support": 0.8,
    "tool_access": 0.9,
    "peer_support": 0.8,
    "workflow_support": 0.85,
}


def evidence(self_value, manager, behavior, objective):
    return [
        {"source": "self", "value": self_value, "confidence": 0.8},
        {"source": "manager", "value": manager, "confidence": 0.9},
        {"source": "behavior", "value": behavior, "confidence": 0.9},
        {"source": "objective", "value": objective, "confidence": 0.95},
    ]


TRAJECTORY = [
    {
        "phase": "baseline",
        "days_after": 0,
        "evidence": evidence(0.45, 0.42, 0.40, 0.44),
    },
    {
        "phase": "followup",
        "days_after": 30,
        "evidence": evidence(0.72, 0.68, 0.70, 0.73),
        "conditions": GOOD_CONDITIONS,
    },
    {
        "phase": "followup",
        "days_after": 60,
        "evidence": evidence(0.70, 0.69, 0.69, 0.71),
        "conditions": GOOD_CONDITIONS,
    },
    {
        "phase": "followup",
        "days_after": 90,
        "evidence": evidence(0.69, 0.67, 0.68, 0.70),
        "conditions": GOOD_CONDITIONS,
    },
]


class CoreTests(unittest.TestCase):
    def test_weights_normalize(self):
        weights = core.validate_evidence_weights(WEIGHTS)
        self.assertAlmostEqual(sum(weights.values()), 1.0)

    def test_weight_keys_must_match_sources(self):
        with self.assertRaises(ValueError):
            core.validate_evidence_weights(
                {"self": 1.0}
            )

    def test_boolean_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            core.aggregate_transfer_evidence(
                [
                    {
                        "source": "self",
                        "value": True,
                        "confidence": 1.0,
                    }
                ]
            )

    def test_nan_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            core.aggregate_transfer_evidence(
                [
                    {
                        "source": "self",
                        "value": math.nan,
                        "confidence": 1.0,
                    }
                ]
            )

    def test_unknown_source_is_rejected(self):
        with self.assertRaises(ValueError):
            core.aggregate_transfer_evidence(
                [
                    {
                        "source": "peer_guess",
                        "value": 0.5,
                        "confidence": 1.0,
                    }
                ]
            )

    def test_confidence_weighting_within_source(self):
        result = core.aggregate_transfer_evidence(
            [
                {
                    "source": "behavior",
                    "value": 0.2,
                    "confidence": 1.0,
                },
                {
                    "source": "behavior",
                    "value": 0.8,
                    "confidence": 0.5,
                },
            ],
            weights={
                "self": 0,
                "manager": 0,
                "behavior": 1,
                "objective": 0,
            },
        )
        self.assertAlmostEqual(
            result["source_scores"]["behavior"],
            (0.2 + 0.4) / 1.5,
        )

    def test_missing_sources_reweight_available_sources(self):
        result = core.aggregate_transfer_evidence(
            [
                {
                    "source": "behavior",
                    "value": 0.7,
                    "confidence": 1.0,
                },
                {
                    "source": "objective",
                    "value": 0.9,
                    "confidence": 1.0,
                },
            ],
            weights=WEIGHTS,
        )
        expected = (
            0.7 * (0.30 / 0.65)
            + 0.9 * (0.35 / 0.65)
        )
        self.assertAlmostEqual(
            result["application_score"],
            expected,
        )

    def test_source_disagreement_is_detected(self):
        result = core.aggregate_transfer_evidence(
            evidence(0.2, 0.8, 0.7, 0.75),
            disagreement_threshold=0.25,
        )
        self.assertTrue(result["disagreement_flag"])
        self.assertGreater(
            result["agreement_range"],
            0.25,
        )

    def test_transfer_conditions_do_not_change_outcome_score(self):
        score = core.aggregate_transfer_evidence(
            evidence(0.8, 0.8, 0.8, 0.8),
        )["application_score"]
        low = core.condition_diagnostics(LOW_OPPORTUNITY)
        high = core.condition_diagnostics(GOOD_CONDITIONS)
        self.assertAlmostEqual(score, 0.8)
        self.assertNotEqual(
            low["barrier_count"],
            high["barrier_count"],
        )

    def test_conditions_require_all_fields(self):
        with self.assertRaises(ValueError):
            core.condition_diagnostics(
                {"manager_support": 0.8}
            )

    def test_condition_barrier_severity(self):
        result = core.condition_diagnostics(
            LOW_OPPORTUNITY,
            review_threshold=0.5,
        )
        self.assertEqual(
            result["barriers"][0]["condition"],
            "opportunity_to_perform",
        )
        self.assertAlmostEqual(
            result["barriers"][0]["severity"],
            0.2,
        )

    def test_baseline_must_use_day_zero(self):
        bad = [
            {
                "phase": "baseline",
                "days_after": 5,
                "evidence": evidence(0.4, 0.4, 0.4, 0.4),
            },
            TRAJECTORY[1],
        ]
        with self.assertRaises(ValueError):
            core.validate_trajectory(bad)

    def test_followup_days_must_be_unique(self):
        bad = [
            TRAJECTORY[0],
            TRAJECTORY[1],
            dict(TRAJECTORY[1]),
        ]
        with self.assertRaises(ValueError):
            core.validate_trajectory(bad)

    def test_trajectory_requires_one_baseline(self):
        with self.assertRaises(ValueError):
            core.validate_trajectory(
                TRAJECTORY[1:]
            )

    def test_trajectory_orders_followups(self):
        shuffled = [
            TRAJECTORY[0],
            TRAJECTORY[3],
            TRAJECTORY[1],
            TRAJECTORY[2],
        ]
        result = core.validate_trajectory(shuffled)
        self.assertEqual(
            [row["days_after"] for row in result],
            [0, 30, 60, 90],
        )

    def test_trajectory_reports_baseline_change(self):
        result = core.analyze_trajectory(
            TRAJECTORY,
            weights=WEIGHTS,
        )
        self.assertGreater(
            result["first_change_from_baseline"],
            0,
        )
        self.assertGreater(
            result["final_change_from_baseline"],
            0,
        )

    def test_persistence_is_observed_not_assumed(self):
        result = core.analyze_trajectory(
            TRAJECTORY,
            weights=WEIGHTS,
        )
        expected = (
            result["final_followup_score"]
            / result["first_followup_score"]
        )
        self.assertAlmostEqual(
            result["observed_persistence_ratio"],
            expected,
        )

    def test_followup_change_can_be_negative(self):
        result = core.analyze_trajectory(
            TRAJECTORY,
            weights=WEIGHTS,
        )
        self.assertLess(
            result["followup_change"],
            0,
        )

    def test_change_per_30_days_available_with_repeated_followup(self):
        result = core.analyze_trajectory(
            TRAJECTORY,
            weights=WEIGHTS,
        )
        self.assertIsNotNone(
            result["change_per_30_days"]
        )

    def test_single_followup_has_no_rate(self):
        result = core.analyze_trajectory(
            TRAJECTORY[:2],
            weights=WEIGHTS,
        )
        self.assertIsNone(
            result["change_per_30_days"]
        )

    def test_low_opportunity_remains_visible_as_barrier(self):
        trajectory = [
            TRAJECTORY[0],
            dict(
                TRAJECTORY[1],
                conditions=LOW_OPPORTUNITY,
            ),
        ]
        result = core.analyze_trajectory(
            trajectory,
            weights=WEIGHTS,
        )
        barriers = result["timepoints"][1][
            "condition_review"
        ]["barriers"]
        self.assertEqual(
            barriers[0]["condition"],
            "opportunity_to_perform",
        )

    def test_cohort_summary(self):
        first = core.analyze_trajectory(
            TRAJECTORY,
            weights=WEIGHTS,
        )
        second = core.analyze_trajectory(
            [
                TRAJECTORY[0],
                dict(
                    TRAJECTORY[1],
                    conditions=LOW_OPPORTUNITY,
                ),
                dict(
                    TRAJECTORY[2],
                    conditions=LOW_OPPORTUNITY,
                ),
            ],
            weights=WEIGHTS,
        )
        summary = core.cohort_summary(
            [first, second]
        )
        self.assertEqual(summary["n"], 2)
        self.assertIn(
            "opportunity_to_perform",
            summary["barrier_counts"],
        )

    def test_empty_cohort_is_rejected(self):
        with self.assertRaises(ValueError):
            core.cohort_summary([])

    def test_weight_sensitivity_returns_ranges(self):
        result = core.weight_sensitivity(
            TRAJECTORY,
            {
                "balanced": WEIGHTS,
                "behavior_heavy": {
                    "self": 0.05,
                    "manager": 0.10,
                    "behavior": 0.55,
                    "objective": 0.30,
                },
                "objective_heavy": {
                    "self": 0.05,
                    "manager": 0.10,
                    "behavior": 0.20,
                    "objective": 0.65,
                },
            },
        )
        self.assertEqual(
            set(result["scenarios"]),
            {
                "balanced",
                "behavior_heavy",
                "objective_heavy",
            },
        )
        self.assertLessEqual(
            result["final_score_range"][0],
            result["final_score_range"][1],
        )

    def test_hypothetical_decay_is_explicit_simulation(self):
        value = core.simulate_hypothetical_decay(
            0.8,
            60,
            half_life=60,
        )
        self.assertAlmostEqual(value, 0.4)

    def test_decay_rejects_boolean_days(self):
        with self.assertRaises(ValueError):
            core.simulate_hypothetical_decay(
                0.8,
                True,
            )

    def test_transfer_index_does_not_multiply_opportunity(self):
        high = core.transfer_index(
            0.8,
            0.7,
            0.9,
            opportunity=1.0,
        )
        low = core.transfer_index(
            0.8,
            0.7,
            0.9,
            opportunity=0.2,
        )
        self.assertAlmostEqual(high, low)

    def test_backward_barrier_flags(self):
        flags = core.barrier_flags(
            0.2,
            0.8,
            0.8,
        )
        self.assertIn(
            "manager_support",
            flags,
        )

    def test_zero_confidence_only_is_rejected(self):
        with self.assertRaises(ValueError):
            core.aggregate_transfer_evidence(
                [
                    {
                        "source": "self",
                        "value": 0.8,
                        "confidence": 0.0,
                    }
                ]
            )

    def test_source_coverage_is_reported(self):
        result = core.aggregate_transfer_evidence(
            [
                {
                    "source": "behavior",
                    "value": 0.7,
                    "confidence": 1.0,
                }
            ],
            weights={
                "self": 0,
                "manager": 0,
                "behavior": 1,
                "objective": 0,
            },
        )
        self.assertEqual(
            result["source_coverage"],
            0.25,
        )


if __name__ == "__main__":
    unittest.main()
