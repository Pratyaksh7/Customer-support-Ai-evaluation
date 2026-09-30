import json

from app.scoring.gate import EvaluationGate


def main():

    with open(
        "config/evaluation_thresholds.json",
        "r",
    ) as file:
        thresholds = json.load(file)

    summary = {
        "overall_score": 0.81,
        "criteria": {
            "correctness": {
                "average_score": 0.85
            },
            "groundedness": {
                "average_score": 0.76
            },
            "relevance": {
                "average_score": 0.90
            },
        },
    }

    gate = EvaluationGate()

    result = gate.check(
        summary,
        thresholds,
    )

    print("=" * 80)
    print("EVALUATION GATE")
    print("=" * 80)

    print(f"PASSED: {result.passed}")

    if result.failures:

        print()
        print("FAILURES:")

        for failure in result.failures:
            print(f"- {failure}")


if __name__ == "__main__":
    main()