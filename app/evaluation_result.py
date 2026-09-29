from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationResult:
    evaluator: str
    criterion: str
    score: float
    passed: bool
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)