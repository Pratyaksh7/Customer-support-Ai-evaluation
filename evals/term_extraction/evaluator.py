from evals.term_extraction.normalizer import normalize_value
from evals.term_extraction.schema_validator import TermSchemaValidator
from evals.term_extraction.field_weights import FIELD_WEIGHTS

class TermExtractionEvaluator:

    def __init__(self):
        self.schema_validator = TermSchemaValidator() 

    def evaluate(
            self,
        expected: dict,
        actual: dict,
    ) -> dict:
        field_results = {}

        for field, expected_value in expected.items():
            actual_value = actual.get(field)

            expected_normalized = normalize_value(field, expected_value)
            actual_normalized = normalize_value(field, actual_value)

            if expected_normalized == actual_normalized:
                status = "PASS"
                reason = "Extracted value matches expected value."

            elif expected_normalized is not None and actual_normalized is None:
                status = "MISSING"
                reason = "Expected value was not extracted."

            elif expected_normalized is None and actual_normalized is not None:
                status = "HALLUCINATED"
                reason = "Model extracted a value that should not be present."

            else:
                status = "INCORRECT"
                reason = "Extracted value does not match expected value."

            field_results[field] = {
                "expected": expected_value,
                "actual": actual_value,
                "status": status,
                "passed": status == "PASS",
                "reason": reason,
            }

        schema_results = self.schema_validator.validate(actual)

        weighted_score = self.calculate_weighted_score(field_results)
        return {
            "fields": field_results,
            "schema": schema_results,
            "weighted_score": weighted_score
        }

    def summarize(self, results: dict,) -> dict:

        field_results = results["fields"]
        schema_results = results["schema"]
        weighted_score = results["weighted_score"]

        total_fields = len(field_results)

        passed = sum(
            1 for result in field_results.values()
            if result["status"] == "PASS"
        )

        missing = sum(
            1 for result in field_results.values()
            if result["status"] == "MISSING"
        )

        incorrect = sum(
            1 for result in field_results.values()
            if result["status"] == "INCORRECT"
        )

        hallucinated = sum(
            1 for result in field_results.values()
            if result["status"] == "HALLUCINATED"
        )

        schema_passed = sum(
            1
            for result in schema_results
            if result["passed"]
        )

        schema_failed = len(schema_results) - schema_passed

        return {
            "fields": {
                "total": total_fields,
                "passed": passed,
                "missing": missing,
                "incorrect": incorrect,
                "hallucinated": hallucinated,
                "score": round(
                    (passed / total_fields) * 100,
                    2
                ) if total_fields else 0.0,
            },
            "schema": {
                "total": len(schema_results),
                "passed": schema_passed,
                "failed": schema_failed,
            },
            "weighted_score": weighted_score,
        }

    def calculate_weighted_score(self, field_results):
        total_weight = 0.0
        earned_weight = 0.0

        for field, result in field_results.items():
            weight = FIELD_WEIGHTS.get(field, 1.0)

            total_weight += weight
            status = result["status"]

            if status == "PASS":
                earned_weight += weight

            elif status == "INCORRECT":
                earned_weight += weight * 0.0

            elif status == "MISSING":
                earned_weight += weight * 0.0

            elif status == "HALLUCINATED":
                earned_weight += weight * 0.0

        if total_weight == 0:
            return 0.0

        return round((earned_weight / total_weight) * 100, 2)