class TermExtractionQualityGate:

    def __init__(
        self,
        min_weighted_score: float = 90.0,
        min_pass_rate: float = 90.0,
        max_hallucinated: int = 0,
        max_schema_failures: int = 0,
    ):
        self.min_weighted_score = min_weighted_score
        self.min_pass_rate = min_pass_rate
        self.max_hallucinated = max_hallucinated
        self.max_schema_failures = max_schema_failures

    def evaluate(self, run_summary: dict) -> dict:
        failures = []

        weighted_score = run_summary["average_weighted_score"]
        pass_rate = run_summary["pass_rate"]
        hallucinated = run_summary["failure_counts"]["hallucinated"]
        schema_failures = run_summary["schema_failures"]

        if weighted_score < self.min_weighted_score:
            failures.append({
                "rule": "minimum_weighted_score",
                "expected": self.min_weighted_score,
                "actual": weighted_score,
                "reason": (
                    f"Weighted score {weighted_score}% "
                    f"is below required {self.min_weighted_score}%."
                ),
            })

        if pass_rate < self.min_pass_rate:
            failures.append({
                "rule": "minimum_pass_rate",
                "expected": self.min_pass_rate,
                "actual": pass_rate,
                "reason": (
                    f"Pass rate {pass_rate}% "
                    f"is below required {self.min_pass_rate}%."
                ),
            })

        if hallucinated > self.max_hallucinated:
            failures.append({
                "rule": "maximum_hallucinations",
                "expected": self.max_hallucinated,
                "actual": hallucinated,
                "reason": (
                    f"Found {hallucinated} hallucinated fields. "
                    f"Maximum allowed is {self.max_hallucinated}."
                ),
            })

        if schema_failures > self.max_schema_failures:
            failures.append({
                "rule": "maximum_schema_failures",
                "expected": self.max_schema_failures,
                "actual": schema_failures,
                "reason": (
                    f"Found {schema_failures} schema failures. "
                    f"Maximum allowed is {self.max_schema_failures}."
                ),
            })

        return {
            "passed": len(failures) == 0,
            "failures": failures,
            "rules": {
                "min_weighted_score": self.min_weighted_score,
                "min_pass_rate": self.min_pass_rate,
                "max_hallucinated": self.max_hallucinated,
                "max_schema_failures": self.max_schema_failures,
            },
        }