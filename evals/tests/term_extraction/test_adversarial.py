import json

from app.llm import LLMClient

from evals.term_extraction.extractor import TermExtractor
from evals.term_extraction.evaluator import TermExtractionEvaluator
from evals.term_extraction.checklist import get_default_checklist


def main():

    with open(
        "evals/datasets/term_extraction_adversarial_cases.json",
        "r",
        encoding="utf-8",
    ) as file:

        cases = json.load(file)

    llm = LLMClient()

    extractor = TermExtractor(llm)
    evaluator = TermExtractionEvaluator()

    passed = 0
    failed = 0

    for case in cases:

        print("=" * 80)
        print(f"CASE: {case['id']}")
        print(f"TYPE: {case['type']}")
        print("=" * 80)

        actual = extractor.extract(
            email=case["email"],
            checklist=get_default_checklist(),
        )

        print("\nRAW EXTRACTOR OUTPUT:")
        print(json.dumps(actual, indent=2))

        result = evaluator.evaluate(
            expected=case["expected_output"],
            actual=actual,
        )

        summary = evaluator.summarize(result)

        score = summary["fields"]

        case_passed = (
            score["passed"] == score["total"]
            and score["hallucinated"] == 0
        )

        if case_passed:
            passed += 1
            print("STATUS: PASS")
        else:
            failed += 1
            print("STATUS: FAIL")

        if not case_passed:
            print(
                f"Passed:       {score['passed']}/"
                f"{score['total']}"
            )
            print(f"Missing:      {score['missing']}")
            print(f"Incorrect:    {score['incorrect']}")
            print(f"Hallucinated: {score['hallucinated']}")

            print("\nFAILED FIELDS:")

            for field, field_result in result["fields"].items():
                if not field_result["passed"]:
                    print(
                        f"- {field}: "
                        f"{field_result['status']}"
                    )
                    print(
                        f"  Expected: "
                        f"{field_result['expected']}"
                    )
                    print(
                        f"  Actual:   "
                        f"{field_result['actual']}"
                    )

    print()
    print("=" * 80)
    print("ADVERSARIAL SUMMARY")
    print("=" * 80)

    print(f"TOTAL:  {len(cases)}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")

    pass_rate = (
        (passed / len(cases)) * 100
        if cases
        else 0
    )

    print(f"PASS RATE: {pass_rate:.2f}%")


if __name__ == "__main__":
    main()