class TermExtractionRegressionComparator:

    def compare(
        self,
        baseline: dict,
        current: dict,
    ) -> dict:

        baseline_summary = baseline["summary"]
        current_summary = current["summary"]

        return {
            "weighted_score": self._score_delta(
                baseline_summary["average_weighted_score"],
                current_summary["average_weighted_score"],
            ),

            "field_score": self._score_delta(
                baseline_summary["average_field_score"],
                current_summary["average_field_score"],
            ),

            "pass_rate": self._score_delta(
                baseline_summary["pass_rate"],
                current_summary["pass_rate"],
            ),

            "missing": self._failure_delta(
                baseline_summary["missing"],
                current_summary["missing"],
            ),

            "incorrect": self._failure_delta(
                baseline_summary["incorrect"],
                current_summary["incorrect"],
            ),

            "hallucinated": self._failure_delta(
                baseline_summary["hallucinated"],
                current_summary["hallucinated"],
            ),

            "schema_failures": self._failure_delta(
                baseline_summary["schema_failures"],
                current_summary["schema_failures"],
            ),
            "fields": self.compare_fields(
                baseline,
                current,
            ),
        }

    def compare_fields(
    self,
    baseline: dict,
    current: dict,
    ) -> dict:

        baseline_fields = baseline["summary"].get(
            "field_performance",
            {}
        )

        current_fields = current["summary"].get(
            "field_performance",
            {}
        )

        fields = set(baseline_fields) | set(current_fields)

        comparison = {}

        for field in sorted(fields):

            baseline_rate = baseline_fields.get(
                field,
                {}
            ).get("pass_rate", 0.0)

            current_rate = current_fields.get(
                field,
                {}
            ).get("pass_rate", 0.0)

            comparison[field] = {
                "baseline": baseline_rate,
                "current": current_rate,
                "delta": round(
                    current_rate - baseline_rate,
                    2,
                ),
            }

        return comparison

    @staticmethod
    def _score_delta(
        baseline: float,
        current: float,
    ) -> dict:

        return {
            "baseline": baseline,
            "current": current,
            "delta": round(current - baseline, 2),
        }

    @staticmethod
    def _failure_delta(
        baseline: int,
        current: int,
    ) -> dict:

        return {
            "baseline": baseline,
            "current": current,
            "delta": current - baseline,
            "improvement": baseline - current,
        }