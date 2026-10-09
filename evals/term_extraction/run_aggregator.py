from statistics import mean
from collections import Counter


class TermExtractionRunAggregator:

    def aggregate(self, case_results: list[dict]) -> dict:
        if not case_results:
            return self._empty_result()

        field_scores = []
        weighted_scores = []

        failure_counts = Counter()
        failure_fields = Counter()

        schema_failures = 0
        passed_cases = 0

        for case_result in case_results:
            summary = case_result["summary"]
            evaluation = case_result["evaluation"]

            field_scores.append(summary["fields"]["score"])
            weighted_scores.append(summary["weighted_score"])

            # --------------------------------------------------
            # Case pass/fail
            # --------------------------------------------------

            case_passed = (
                summary["weighted_score"] == 100
                and summary["fields"]["hallucinated"] == 0
                and summary["fields"]["incorrect"] == 0
                and summary["fields"]["missing"] == 0
            )

            if case_passed:
                passed_cases += 1

            # --------------------------------------------------
            # Failure types + fields
            # --------------------------------------------------

            for field, result in evaluation["fields"].items():
                status = result["status"]

                if status != "PASS":
                    failure_counts[status] += 1
                    failure_fields[field] += 1

            # --------------------------------------------------
            # Schema failures
            # --------------------------------------------------

            for schema_result in evaluation.get("schema", []):
                if not schema_result["passed"]:
                    schema_failures += 1

        total_cases = len(case_results)
        field_performance = self.aggregate_field_performance(case_results)

        return {
            "total_cases": total_cases,
            "passed_cases": passed_cases,
            "failed_cases": total_cases - passed_cases,

            "pass_rate": round(
                (passed_cases / total_cases) * 100,
                2,
            ),

            "average_field_score": round(
                mean(field_scores),
                2,
            ),

            "average_weighted_score": round(
                mean(weighted_scores),
                2,
            ),

            "failure_counts": {
                "missing": failure_counts["MISSING"],
                "incorrect": failure_counts["INCORRECT"],
                "hallucinated": failure_counts["HALLUCINATED"],
            },

            "failure_fields": dict(
                failure_fields
            ),

            "schema_failures": schema_failures,
            "field_performance": field_performance,
        }

    def aggregate_field_performance(
        self,
        case_results: list[dict],
    ) -> dict:
        field_stats = {}

        for case_result in case_results:

            for field, result in case_result["evaluation"]["fields"].items():

                if field not in field_stats:
                    field_stats[field] = {
                        "total": 0,
                        "passed": 0,
                        "missing": 0,
                        "incorrect": 0,
                        "hallucinated": 0,
                    }

                stats = field_stats[field]

                stats["total"] += 1

                status = result["status"]

                if status == "PASS":
                    stats["passed"] += 1

                elif status == "MISSING":
                    stats["missing"] += 1

                elif status == "INCORRECT":
                    stats["incorrect"] += 1

                elif status == "HALLUCINATED":
                    stats["hallucinated"] += 1

        for field, stats in field_stats.items():

            stats["pass_rate"] = round(
                (stats["passed"] / stats["total"]) * 100,
                2,
            ) if stats["total"] else 0.0

        return field_stats

    def _empty_result(self) -> dict:
        return {
            "total_cases": 0,
            "passed_cases": 0,
            "failed_cases": 0,
            "pass_rate": 0.0,
            "average_field_score": 0.0,
            "average_weighted_score": 0.0,
            "failure_counts": {
                "missing": 0,
                "incorrect": 0,
                "hallucinated": 0,
            },
            "failure_fields": {},
            "schema_failures": 0,
        }