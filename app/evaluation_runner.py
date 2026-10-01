from app.evaluation_engine import EvaluationEngine
from app.evaluators.llm import LLMEvaluator
from app.scoring.aggregator import EvaluationAggregator
from app.scoring.case_result import CaseEvaluation
from app.scoring.gate import EvaluationGate

# EvaluationRunner
#       │
#       ├── EvaluationEngine
#       │       └── deterministic
#       │
#       └── LLMEvaluator
#               └── LLM

class EvaluationRunner:

    def __init__(
        self,
        evaluation_engine: EvaluationEngine,
        llm_evaluator: LLMEvaluator,
        aggregator: EvaluationAggregator,
        gate: EvaluationGate,
    ):
        self.evaluation_engine = evaluation_engine
        self.llm_evaluator = llm_evaluator
        self.aggregator = aggregator
        self.gate = gate

    def evaluate_case(
        self,
        case: dict,
        answer: str,
    ) -> CaseEvaluation:

        results = []

        deterministic_rules = case.get(
            "deterministic_rules",
            []
        )

        if deterministic_rules:

            results.extend(
                self.evaluation_engine.evaluate(
                    answer=answer,
                    rules=deterministic_rules,
                )
            )

        results.extend(
            self.llm_evaluator.evaluate(
                question=case["question"],
                answer=answer,
                source_of_truth=case["source_of_truth"],
                expected_facts=case["expected_facts"],
            )
        )

        return CaseEvaluation(
            case_id=case["id"],
            question=case["question"],
            answer=answer,
            results=results,
        )

    def summarize(self, case_evaluations: list[CaseEvaluation]):

        evaluation_results = []

        for case_evaluation in case_evaluations:

            evaluation_results.extend(
                case_evaluation.results
            )

        return self.aggregator.aggregate(
            evaluation_results
        )

    def check_gate(
        self,
        summary,
        thresholds,
    ):
        return self.gate.check(
            summary,
            thresholds,
        )