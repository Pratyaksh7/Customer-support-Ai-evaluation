from app.run_store import RunStore
from app.scoring.comparator import EvaluationComparator


def main():

    store = RunStore()

    runs = store.list_runs()

    if len(runs) < 2:

        print(
            "Need at least 2 evaluation runs."
        )

        print(
            "Run `python main.py` again."
        )

        return

    baseline_id = runs[-2]
    current_id = runs[-1]

    baseline = store.load(
        baseline_id
    )

    current = store.load(
        current_id
    )

    comparator = EvaluationComparator()

    print("=" * 80)
    print("EVALUATION RUN COMPARISON")
    print("=" * 80)

    print(
        f"BASELINE: {baseline_id}"
    )

    print(
        f"CURRENT:  {current_id}"
    )

    print()

    overall = comparator.compare_overall(
        baseline["summary"],
        current["summary"],
    )

    print("OVERALL QUALITY")
    print(
        f"{overall['baseline']:.3f}"
        f" → "
        f"{overall['current']:.3f}"
        f" "
        f"({overall['change']:+.3f})"
    )

    print()

    print("METRIC CHANGES")

    changes = comparator.compare_summary(
        baseline["summary"],
        current["summary"],
    )

    for change in changes:

        status = "UNCHANGED"

        if change.improved:
            status = "IMPROVED"

        elif change.regressed:
            status = "REGRESSED"

        print(
            f"{change.metric.upper():15}"
            f"{change.baseline:.3f}"
            f" → "
            f"{change.current:.3f}"
            f" "
            f"({change.change:+.3f})"
            f"  [{status}]"
        )

    print()
    print("=" * 80)
    print("CASE-LEVEL CHANGES")
    print("=" * 80)

    case_comparisons = (
        comparator.compare_cases(
            baseline,
            current,
        )
    )

    for case in case_comparisons:

        regressions = [
            metric
            for metric in case["metrics"]
            if metric["change"] < 0
        ]

        improvements = [
            metric
            for metric in case["metrics"]
            if metric["change"] > 0
        ]

        if not regressions and not improvements:
            continue

        print()
        print(
            f"CASE: {case['case_id']}"
        )

        for metric in case["metrics"]:

            if metric["change"] == 0:
                continue

            status = (
                "IMPROVED"
                if metric["change"] > 0
                else "REGRESSED"
            )

            print(
                f"  {metric['criterion']}: "
                f"{metric['baseline']:.3f}"
                f" → "
                f"{metric['current']:.3f}"
                f" "
                f"({metric['change']:+.3f})"
                f" [{status}]"
            )


if __name__ == "__main__":
    main()