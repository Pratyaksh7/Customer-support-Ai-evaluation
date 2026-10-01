import json
from datetime import datetime
from dataclasses import asdict

from app.run import EvaluationRun
from app.run_store import RunStore

from app.customer_support import CustomerSupportAgent
from app.evaluator import AnswerEvaluator
from app.evaluation_engine import EvaluationEngine
from app.evaluation_runner import EvaluationRunner
from app.evaluators.deterministic import DeterministicEvaluator
from app.evaluators.llm import LLMEvaluator
from app.scoring.aggregator import EvaluationAggregator
from app.scoring.gate import EvaluationGate
from app.llm import LLMClient

def create_run_id() -> str:

    return datetime.now().strftime(
        "run_%Y%m%d_%H%M%S"
    )

def load_evaluation_cases():
    with open(
        "data/evaluation_cases.json",
        "r",
    ) as file:
        return json.load(file)


def load_thresholds():
    with open(
        "config/evaluation_thresholds.json",
        "r",
    ) as file:
        return json.load(file)


def build_evaluation_runner(llm):

    deterministic_evaluator = DeterministicEvaluator()

    evaluation_engine = EvaluationEngine(
        deterministic_evaluator=deterministic_evaluator
    )

    existing_llm_evaluator = AnswerEvaluator(llm)

    llm_evaluator = LLMEvaluator(existing_llm_evaluator)

    aggregator = EvaluationAggregator()

    gate = EvaluationGate()

    return EvaluationRunner(
        evaluation_engine=evaluation_engine,
        llm_evaluator=llm_evaluator,
        aggregator=aggregator,
        gate=gate,
    )


def main():

    llm = LLMClient()

    agent = CustomerSupportAgent(
        llm
    )

    runner = build_evaluation_runner(
        llm
    )

    cases = load_evaluation_cases()

    thresholds = load_thresholds()

    all_results = []

    for case in cases:

        print("=" * 80)

        print(
            f"CASE: {case['id']}"
        )

        print(
            f"QUESTION: {case['question']}"
        )

        print()

        # -----------------------------
        # Generate answer
        # -----------------------------

        answer = agent.answer(
            case["question"]
        )

        print("AI ANSWER:")
        print(answer)

        print()

        # -----------------------------
        # Evaluate
        # -----------------------------

        case_evaluation = runner.evaluate_case(
            case=case,
            answer=answer,
        )

        all_results.append(case_evaluation)

        # all_results.extend(case_evaluation.results)

        # -----------------------------
        # Print case results
        # -----------------------------

        print("EVALUATION:")

        for result in case_evaluation.results:

            display_score = (
                result.metadata.get(
                    "raw_score",
                    result.score
                )
            )

            print(
                f"{result.criterion.upper()}: "
                f"{display_score}"
            )

            print(
                f"Reason: {result.reason}"
            )

            print()

    # ---------------------------------
    # Aggregate entire dataset
    # ---------------------------------

    summary = runner.summarize(
        all_results
    )

    print("=" * 80)
    print("DATASET SUMMARY")
    print("=" * 80)

    print(
        f"Quality score: "
        f"{summary['quality_score']}"
    )

    print(
        f"Deterministic score: "
        f"{summary['deterministic_score']}"
    )

    print(
        f"Total evaluations: "
        f"{summary['total_evaluations']}"
    )

    print()

    print("QUALITY METRICS:")

    for criterion, data in (
        summary["criteria"].items()
    ):

        print(
            f"{criterion.upper()}: "
            f"{data['average_score']}"
        )

    print("DETERMINISTIC:")

    for criterion, data in (
        summary["deterministic"].items()
    ):

        print(
            f"{criterion.upper()}: "
            f"{data['pass_rate']}"
        )

    # ---------------------------------
    # Quality gate
    # ---------------------------------

    gate_result = runner.check_gate(
        summary=summary,
        thresholds=thresholds,
    )

    print()

    print("=" * 80)
    print("QUALITY GATE")
    print("=" * 80)

    print(
        f"PASSED: {gate_result.passed}"
    )

    if gate_result.failures:

        print()

        for failure in (
            gate_result.failures
        ):
            print(
                f"- {failure}"
            )

    serialized_results = [
                asdict(result)
                for result in all_results
            ]
    
    run = EvaluationRun(
        run_id=create_run_id(),
        timestamp=datetime.now().isoformat(),

        cases_evaluated=len(cases),

        results=serialized_results,

        summary=summary,

        quality_gate={
            "passed": gate_result.passed,
            "failures": gate_result.failures,
        },
    )

    store = RunStore()

    file_path = store.save(run)

    print()
    print(
        f"Evaluation run saved to: "
        f"{file_path}"
    )

if __name__ == "__main__":
    main()