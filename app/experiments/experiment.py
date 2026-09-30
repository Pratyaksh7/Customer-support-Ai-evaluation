from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Experiment:
    name: str
    agent_version: str
    results: dict
    timestamp: str = field(
        default_factory=lambda:
        datetime.now().isoformat()
    )