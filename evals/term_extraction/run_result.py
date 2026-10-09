import uuid
from datetime import datetime


def build_run_result(
    case_results: list[dict],
    run_summary: dict,
    quality_result: dict,
) -> dict:

    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),

        "evaluation": {
            "type": "term_extraction",
        },

        "summary": run_summary,

        "quality_gate": quality_result,

        "cases": case_results,
    }