from app.evaluation_result import EvaluationResult


class LLMEvaluator:

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def evaluate(
        self,
        question: str,
        answer: str,
        source_of_truth: list[str],
    ) -> list[EvaluationResult]:

        evaluation = self.evaluator.evaluate(
            question=question,
            ai_answer=answer,
            source_of_truth=source_of_truth,
        )

        results = []

        for criterion, result in evaluation.items():

            results.append(
                EvaluationResult(
                    evaluator="llm",
                    criterion=criterion,
                    score=result["score"],
                    passed=result["score"] >= 4,
                    reason=result["reason"],
                )
            )

        return results