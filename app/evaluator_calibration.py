import json

from app.evaluator import AnswerEvaluator


class EvaluatorCalibration:
    def __init__(self, evaluator: AnswerEvaluator):
        self.evaluator = evaluator

    def load_cases(self):
        with open("data/calibration_cases.json", "r") as file:
            return json.load(file)

    def compare_scores(self, expected, actual):
        difference = abs(expected - actual)

        if difference == 0:
            return "EXACT"

        if difference == 1:
            return "NEAR"

        return "SIGNIFICANT_DISAGREEMENT"

    def run(self):
        cases = self.load_cases()

        for case in cases:
            print("=" * 80)
            print(f"CALIBRATION CASE: {case['id']}")

            actual = self.evaluator.evaluate(
                question=case["question"],
                ai_answer=case["ai_answer"],
                source_of_truth=case["source_of_truth"],
                expected_facts=[]
            )

            expected = case["expected_evaluation"]

            print()
            print("EXPECTED vs ACTUAL")
            print()

            for criterion, expected_score in expected.items():

                actual_score = actual[criterion]["score"]

                result = self.compare_scores(
                    expected_score,
                    actual_score
                )

                print(
                    f"{criterion.upper()}: "
                    f"expected={expected_score}, "
                    f"actual={actual_score}, "
                    f"{result}"
                )