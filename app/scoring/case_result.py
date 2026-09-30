from dataclasses import dataclass

from app.evaluation_result import EvaluationResult


@dataclass
class CaseEvaluation:
    case_id: str
    question: str
    answer: str
    results: list[EvaluationResult]