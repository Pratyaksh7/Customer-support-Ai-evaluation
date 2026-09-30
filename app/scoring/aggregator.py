from collections import defaultdict
from statistics import mean

from app.evaluation_result import EvaluationResult


class EvaluationAggregator:

    def aggregate(
        self,
        results: list[EvaluationResult],
    ) -> dict:

        quality_scores = defaultdict(list)
        deterministic_scores = defaultdict(list)

        for result in results:

            if result.evaluator == "llm":
                quality_scores[
                    result.criterion
                ].append(result.score)

            elif result.evaluator == "deterministic":
                deterministic_scores[
                    result.criterion
                ].append(result.score)

        # -----------------------------------------
        # Quality metrics
        # -----------------------------------------

        quality_criteria = {}

        for criterion, scores in quality_scores.items():

            quality_criteria[criterion] = {
                "average_score": round(
                    mean(scores),
                    3,
                ),
                "total_evaluations": len(scores),
                "passed": sum(
                    1
                    for score in scores
                    if score >= 0.75
                ),
                "failed": sum(
                    1
                    for score in scores
                    if score < 0.75
                ),
            }

        # -----------------------------------------
        # Deterministic metrics
        # -----------------------------------------

        deterministic_criteria = {}

        for criterion, scores in deterministic_scores.items():

            deterministic_criteria[criterion] = {
                "pass_rate": round(
                    mean(scores),
                    3,
                ),
                "total_evaluations": len(scores),
                "passed": sum(
                    1
                    for score in scores
                    if score == 1.0
                ),
                "failed": sum(
                    1
                    for score in scores
                    if score == 0.0
                ),
            }

        # -----------------------------------------
        # Overall quality score
        # -----------------------------------------

        all_quality_scores = [
            score
            for scores in quality_scores.values()
            for score in scores
        ]

        quality_score = (
            mean(all_quality_scores)
            if all_quality_scores
            else 0.0
        )

        # -----------------------------------------
        # Deterministic pass rate
        # -----------------------------------------

        all_deterministic_scores = [
            score
            for scores in deterministic_scores.values()
            for score in scores
        ]

        deterministic_score = (
            mean(all_deterministic_scores)
            if all_deterministic_scores
            else 1.0
        )

        return {
            "quality_score": round(
                quality_score,
                3,
            ),
            "deterministic_score": round(
                deterministic_score,
                3,
            ),
            "overall_score": round(
                quality_score,
                3,
            ),
            "total_evaluations": len(results),
            "criteria": dict(
                quality_criteria
            ),
            "deterministic": dict(
                deterministic_criteria
            ),
        }