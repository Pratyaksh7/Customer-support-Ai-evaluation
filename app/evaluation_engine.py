from app.evaluation_result import EvaluationResult
from app.evaluators.deterministic import DeterministicEvaluator


class EvaluationEngine:

    def __init__(
        self,
        deterministic_evaluator: DeterministicEvaluator,
    ):
        self.deterministic = deterministic_evaluator

    def evaluate(
        self,
        answer: str,
        rules: list[dict],
    ) -> list[EvaluationResult]:

        results = []

        for rule in rules:
            rule_type = rule["type"]

            if rule_type == "contains":
                result = self.deterministic.contains(
                    answer,
                    rule["expected"],
                )

            elif rule_type == "regex":
                result = self.deterministic.regex(
                    answer,
                    rule["pattern"],
                )

            elif rule_type == "max_length":
                result = self.deterministic.max_length(
                    answer,
                    rule["maximum"],
                )

            elif rule_type == "min_length":
                result = self.deterministic.min_length(
                    answer,
                    rule["minimum"],
                )

            else:
                raise ValueError(
                    f"Unknown evaluation rule: {rule_type}"
                )

            results.append(result)

        return results