import json

from app.llm import LLMClient
from evals.term_extraction.extractor import TermExtractor

from evals.term_extraction.checklist import get_default_checklist

EMAIL = """
Hi,

We are working with a GP who has direct cap table access to Erebor Bank.

Erebor is a new, founder-built national bank focused on capital-intensive
technology sectors, including AI, defense, advanced manufacturing, and crypto.

Allocation available: $40M
Valuation: $8B
Dataroom access is available

Best,
"""

def main():

    with open(
        "evals/datasets/term_extraction_cases.json",
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    llm = LLMClient()

    extractor = TermExtractor(
        llm
    )

    for case in cases:
        print("=" * 80)
        print(f"CASE: {case['id']}")
        print("=" * 80)

        result = extractor.extract(
            email=case["email"],
            checklist=get_default_checklist(),
        )

        for field, value in result.items():

            print(
                f"{field}: {value}"
            )

        print()


if __name__ == "__main__":
    main()

#  python -m evals.tests.term_extraction.test_basic_extraction