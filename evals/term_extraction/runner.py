import json


class TermExtractionRunner:

    def __init__(
        self,
        extractor,
        evaluator,
        aggregator,
        quality_gate,
        checklist,
    ):
        self.extractor = extractor
        self.evaluator = evaluator
        self.aggregator = aggregator
        self.quality_gate = quality_gate
        self.checklist = checklist

    def run(self, dataset_path: str, dataset_type: str = "golden",) -> dict:

        with open(
            dataset_path,
            "r",
            encoding="utf-8",
        ) as file:
            cases = json.load(file)

        case_results = []

        for case in cases:

            actual = self.extractor.extract(
                email=case["email"],
                checklist=self.checklist,
            )

            evaluation = self.evaluator.evaluate(
                expected=case["expected_output"],
                actual=actual,
            )

            summary = self.evaluator.summarize(
                evaluation
            )

            schema_results = evaluation.get("schema", [])

            for schema_result in schema_results:
                if not schema_result["passed"]:
                    print(
                        f"SCHEMA FAILURE: "
                        f"{schema_result['field']} - "
                        f"{schema_result['reason']}"
                    )

            case_results.append({
                "case_id": case["id"],
                "dataset_type": dataset_type,
                "evaluation": evaluation,
                "summary": summary,
            })

        run_summary = self.aggregator.aggregate(
            case_results
        )

        quality_result = self.quality_gate.evaluate(
            run_summary
        )

        return {
            "dataset_type": dataset_type,
            "cases": case_results,
            "summary": run_summary,
            "quality_gate": quality_result,
        }