from dataclasses import dataclass


@dataclass
class MetricChange:
    metric: str
    baseline: float
    current: float
    change: float
    improved: bool
    regressed: bool


class EvaluationComparator:

    def compare(
        self,
        baseline: dict,
        current: dict,
    ) -> list[MetricChange]:

        changes = []

        baseline_criteria = baseline.get(
            "criteria",
            {}
        )

        current_criteria = current.get(
            "criteria",
            {}
        )

        metrics = set(baseline_criteria) | set(current_criteria)

        for metric in metrics:

            baseline_score = baseline_criteria.get(
                metric,
                {}
            ).get(
                "average_score",
                0.0
            )

            current_score = current_criteria.get(
                metric,
                {}
            ).get(
                "average_score",
                0.0
            )

            change = current_score - baseline_score

            changes.append(
                MetricChange(
                    metric=metric,
                    baseline=baseline_score,
                    current=current_score,
                    change=round(change, 3),
                    improved=change > 0,
                    regressed=change < 0,
                )
            )

        return changes

    def compare_overall(
        self,
        baseline: dict,
        current: dict,
    ) -> dict:

        baseline_score = baseline.get(
            "overall_score",
            0.0
        )

        current_score = current.get(
            "overall_score",
            0.0
        )

        change = current_score - baseline_score

        return {
            "baseline": baseline_score,
            "current": current_score,
            "change": round(change, 3),
            "improved": change > 0,
            "regressed": change < 0,
        }