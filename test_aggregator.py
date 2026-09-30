from app.evaluation_result import EvaluationResult
from app.scoring.aggregator import EvaluationAggregator


def main():

    results = [
        EvaluationResult(
            evaluator="llm",
            criterion="correctness",
            score=0.75,
            passed=True,
            reason="Mostly correct.",
        ),
        EvaluationResult(
            evaluator="llm",
            criterion="correctness",
            score=1.0,
            passed=True,
            reason="Fully correct.",
        ),
        EvaluationResult(
            evaluator="llm",
            criterion="relevance",
            score=1.0,
            passed=True,
            reason="Directly answers the question.",
        ),
        EvaluationResult(
            evaluator="llm",
            criterion="relevance",
            score=0.5,
            passed=False,
            reason="Contains irrelevant information.",
        ),
        EvaluationResult(
            evaluator="deterministic",
            criterion="max_length",
            score=1.0,
            passed=True,
            reason="Within limit.",
        ),
    ]

    aggregator = EvaluationAggregator()

    summary = aggregator.aggregate(results)

    print("=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)

    print(f"Overall score: {summary['overall_score']}")
    print(f"Total evaluations: {summary['total_evaluations']}")

    print()

    for criterion, data in summary["criteria"].items():

        print(criterion.upper())

        print(
            f"  Average score: "
            f"{data['average_score']}"
        )

        print(
            f"  Evaluations: "
            f"{data['total_evaluations']}"
        )

        print(
            f"  Passed: "
            f"{data['passed']}"
        )

        print(
            f"  Failed: "
            f"{data['failed']}"
        )

        print()


if __name__ == "__main__":
    main()