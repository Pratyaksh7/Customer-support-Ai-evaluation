from app.scoring.comparator import EvaluationComparator


def main():

    baseline = {
        "overall_score": 0.72,
        "criteria": {
            "correctness": {
                "average_score": 0.70
            },
            "relevance": {
                "average_score": 0.85
            },
            "groundedness": {
                "average_score": 0.60
            },
            "completeness": {
                "average_score": 0.75
            },
        },
    }

    current = {
        "overall_score": 0.81,
        "criteria": {
            "correctness": {
                "average_score": 0.82
            },
            "relevance": {
                "average_score": 0.80
            },
            "groundedness": {
                "average_score": 0.78
            },
            "completeness": {
                "average_score": 0.84
            },
        },
    }

    comparator = EvaluationComparator()

    print("=" * 80)
    print("OVERALL COMPARISON")
    print("=" * 80)

    overall = comparator.compare_overall(
        baseline,
        current,
    )

    print(overall)

    print()
    print("=" * 80)
    print("METRIC COMPARISON")
    print("=" * 80)

    changes = comparator.compare(
        baseline,
        current,
    )

    for change in changes:

        print(
            f"{change.metric}: "
            f"{change.baseline:.3f} → "
            f"{change.current:.3f} "
            f"({change.change:+.3f})"
        )


if __name__ == "__main__":
    main()