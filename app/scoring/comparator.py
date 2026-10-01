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

    def compare_summary(
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

        metrics = (
            set(baseline_criteria)
            | set(current_criteria)
        )

        for metric in sorted(metrics):

            baseline_score = (
                baseline_criteria
                .get(metric, {})
                .get("average_score", 0.0)
            )

            current_score = (
                current_criteria
                .get(metric, {})
                .get("average_score", 0.0)
            )

            change = (
                current_score
                - baseline_score
            )

            changes.append(
                MetricChange(
                    metric=metric,
                    baseline=baseline_score,
                    current=current_score,
                    change=round(
                        change,
                        3,
                    ),
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
            "quality_score",
            0.0,
        )

        current_score = current.get(
            "quality_score",
            0.0,
        )

        change = (
            current_score
            - baseline_score
        )

        return {
            "baseline": baseline_score,
            "current": current_score,
            "change": round(
                change,
                3,
            ),
            "improved": change > 0,
            "regressed": change < 0,
        }

    def compare_cases(
    self,
    baseline_run: dict,
    current_run: dict,
    ) -> list[dict]:

        baseline_cases = {
            case["case_id"]: case
            for case in baseline_run["results"]
        }

        current_cases = {
            case["case_id"]: case
            for case in current_run["results"]
        }

        comparisons = []

        common_cases = (
            set(baseline_cases)
            & set(current_cases)
        )

        for case_id in sorted(common_cases):

            baseline_case = (
                baseline_cases[case_id]
            )

            current_case = (
                current_cases[case_id]
            )

            baseline_results = {
                result["criterion"]: result
                for result
                in baseline_case["results"]
            }

            current_results = {
                result["criterion"]: result
                for result
                in current_case["results"]
            }

            metric_changes = []

            common_metrics = (
                set(baseline_results)
                & set(current_results)
            )

            for metric in sorted(common_metrics):

                baseline_score = (
                    baseline_results[metric]
                    ["score"]
                )

                current_score = (
                    current_results[metric]
                    ["score"]
                )

                change = (
                    current_score
                    - baseline_score
                )

                metric_changes.append({
                    "criterion": metric,
                    "baseline": baseline_score,
                    "current": current_score,
                    "change": round(
                        change,
                        3,
                    ),
                })

            comparisons.append({
                "case_id": case_id,
                "question": current_case[
                    "question"
                ],
                "metrics": metric_changes,
            })

        return comparisons