import json

from app.evaluation_engine import EvaluationEngine
from app.evaluators.deterministic import DeterministicEvaluator


def load_rules():
    with open(
        "data/deterministic_rules.json",
        "r",
    ) as file:
        return json.load(file)


def main():

    evaluator = DeterministicEvaluator()

    engine = EvaluationEngine(
        deterministic_evaluator=evaluator
    )

    answer = """
    Yes, the customer can request a refund.
    The product must be unused and purchased within 30 days.
    """

    rules = load_rules()

    results = engine.evaluate(
        answer=answer,
        rules=rules,
    )

    print("=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)

    for result in results:
        print()
        print(f"Evaluator: {result.evaluator}")
        print(f"Criterion: {result.criterion}")
        print(f"Score: {result.score}")
        print(f"Passed: {result.passed}")
        print(f"Reason: {result.reason}")
        print(f"Metadata: {result.metadata}")


if __name__ == "__main__":
    main()