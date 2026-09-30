from app.evaluation_result import EvaluationResult


class LLMEvaluator:

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def evaluate(
        self,
        question: str,
        answer: str,
        source_of_truth: list[str],
        expected_facts: list[str],
    ) -> list[EvaluationResult]:

        evaluation = self.evaluator.evaluate(
            question=question,
            ai_answer=answer,
            source_of_truth=source_of_truth,
            expected_facts=expected_facts,
        )

        results = []

        for criterion, result in evaluation.items():

            results.append(
                EvaluationResult(
                    evaluator="llm",
                    criterion=criterion,
                    score=(result["score"] - 1) / 4,  # Normalize to 0-1 scale
                    passed=result["score"] >= 4,
                    reason=result["reason"],
                    metadata={
                        "raw_score": result["score"],
                    },
                )
            )

        return results