from dataclasses import dataclass


@dataclass
class GateResult:
    passed: bool
    failures: list[str]


class EvaluationGate:

    def check(
        self,
        summary: dict,
        thresholds: dict,
    ) -> GateResult:

        failures = []

        overall_score = summary.get(
            "quality_score",
            0.0
        )

        minimum_overall = thresholds.get(
            "quality_score"
        )

        if (
            minimum_overall is not None
            and overall_score < minimum_overall
        ):
            failures.append(
                f"Overall score {overall_score} "
                f"is below required "
                f"{minimum_overall}"
            )

        criteria = summary.get(
            "criteria",
            {}
        )

        for criterion, minimum in thresholds.get(
            "criteria",
            {}
        ).items():

            actual = criteria.get(
                criterion,
                {}
            ).get(
                "average_score"
            )

            if actual is None:
                failures.append(
                    f"Missing evaluation metric: "
                    f"{criterion}"
                )
                continue

            if actual < minimum:

                failures.append(
                    f"{criterion} score "
                    f"{actual} is below required "
                    f"{minimum}"
                )

        return GateResult(
            passed=len(failures) == 0,
            failures=failures,
        )