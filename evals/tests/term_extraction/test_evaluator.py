from app.llm import LLMClient

from evals.term_extraction.extractor import TermExtractor
from evals.term_extraction.evaluator import TermExtractionEvaluator
from evals.term_extraction.checklist import get_default_checklist
from evals.term_extraction.run_aggregator import (
    TermExtractionRunAggregator,
)
from evals.term_extraction.quality_gate import (
    TermExtractionQualityGate,
)
from evals.term_extraction.runner import (
    TermExtractionRunner,
)


def main():

    llm = LLMClient()

    extractor = TermExtractor(llm)
    evaluator = TermExtractionEvaluator()
    aggregator = TermExtractionRunAggregator()

    quality_gate = TermExtractionQualityGate(
        min_weighted_score=90.0,
        min_pass_rate=90.0,
        max_hallucinated=0,
        max_schema_failures=0,
    )

    runner = TermExtractionRunner(
        extractor=extractor,
        evaluator=evaluator,
        aggregator=aggregator,
        quality_gate=quality_gate,
        checklist=get_default_checklist(),
    )

    golden_result = runner.run(dataset_path="evals/datasets/term_extraction_cases.json", dataset_type="golden")

    # # Added Temporarily
    # for case_result in golden_result["cases"]:
    #     evaluation = case_result["evaluation"]

    #     failed_fields = {
    #         field: result
    #         for field, result in evaluation["fields"].items()
    #         if not result["passed"]
    #     }

    #     if failed_fields:
    #         print("\n" + "=" * 80)
    #         print(f"FAILURES: {case_result['case_id']}")
    #         print("=" * 80)

    #         for field, result in failed_fields.items():
    #             print(f"\nFIELD: {field}")
    #             print(f"Expected: {result['expected']}")
    #             print(f"Actual:   {result['actual']}")
    #             print(f"Status:   {result['status']}")
    #             print(f"Reason:   {result['reason']}")

    adversarial_result = runner.run(dataset_path="evals/datasets/term_extraction_adversarial_cases.json", dataset_type="adversarial")

    print_run_result("GOLDEN DATASET",golden_result)
    print_run_result("ADVERSARIAL DATASET",adversarial_result)



def print_run_result(title: str, result: dict):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)

    for case in result["cases"]:

        fields = case["summary"]["fields"]

        print(
            f"{case['case_id']:<15} "
            f"{fields['passed']}/"
            f"{fields['total']} passed"
        )

    summary = result["summary"]

    print()
    print(
        f"Cases:             "
        f"{summary['total_cases']}"
    )

    print(
        f"Pass rate:         "
        f"{summary['pass_rate']}%"
    )

    print(
        f"Field score:       "
        f"{summary['average_field_score']}%"
    )

    print(
        f"Weighted score:    "
        f"{summary['average_weighted_score']}%"
    )

    print(
        f"Missing:           "
        f"{summary['failure_counts']['missing']}"
    )

    print(
        f"Incorrect:         "
        f"{summary['failure_counts']['incorrect']}"
    )

    print(
        f"Hallucinated:      "
        f"{summary['failure_counts']['hallucinated']}"
    )

    print(
        f"Schema failures:   "
        f"{summary['schema_failures']}"
    )

    quality = result["quality_gate"]

    print()
    print(
        f"QUALITY GATE: "
        f"{'PASS' if quality['passed'] else 'FAIL'}"
    )


if __name__ == "__main__":
    main()

    #  python -m evals.tests.term_extraction.test_evaluator