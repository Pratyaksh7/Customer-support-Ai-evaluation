class TermExtractionAdversarialEvaluator:

    def evaluate(self, case: dict, actual: dict) -> dict:
        failures = []

        expected = case.get("expected_output", {})

        # Expected fields must match
        for field, expected_value in expected.items():

            actual_value = actual.get(field)

            if actual_value != expected_value:
                failures.append({
                    "type": "incorrect_extraction",
                    "field": field,
                    "expected": expected_value,
                    "actual": actual_value,
                })

        # Explicit anti-hallucination checks
        for field, expected_value in expected.items():

            if expected_value is not None:
                continue

            if actual.get(field) is not None:
                failures.append({
                    "type": "hallucination",
                    "field": field,
                    "actual": actual.get(field),
                })

        return {
            "passed": len(failures) == 0,
            "failures": failures,
        }