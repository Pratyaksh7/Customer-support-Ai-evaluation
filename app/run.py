from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class EvaluationRun:

    run_id: str
    timestamp: str

    cases_evaluated: int

    results: list[dict[str, Any]]

    summary: dict[str, Any]

    quality_gate: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)