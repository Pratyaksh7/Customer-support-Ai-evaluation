from app.evaluators.deterministic import DeterministicEvaluator


def main():
    evaluator = DeterministicEvaluator()

    print("=" * 80)
    print("TEST 1: CONTAINS")
    print("=" * 80)

    result = evaluator.contains(
        "Refunds are processed within 5 business days.",
        "Refunds are processed within 5 business days.",
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 2: CONTAINS - SHOULD FAIL")
    print("=" * 80)

    result = evaluator.contains(
        "Refunds are processed within 5 business days.",
        "Refunds are processed within 10 business days.",
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 3: REGEX")
    print("=" * 80)

    result = evaluator.regex(
        "Revenue: $25M",
        r"\$[\d.]+M",
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 4: REGEX - SHOULD FAIL")
    print("=" * 80)

    result = evaluator.regex(
        "Revenue: 25 million dollars",
        r"\$[\d.]+M",
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 5: MAX LENGTH")
    print("=" * 80)

    result = evaluator.max_length(
        "This is a short answer.",
        100,
    )

    print(result)

    print()
    print("=" * 80)
    print("TEST 6: MIN LENGTH")
    print("=" * 80)

    result = evaluator.min_length(
        "This is a valid answer.",
        5,
    )

    print(result)


if __name__ == "__main__":
    main()