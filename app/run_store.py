import json
from pathlib import Path

from app.run import EvaluationRun


class RunStore:

    def __init__(
        self,
        directory: str = "runs",
    ):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        run: EvaluationRun,
    ) -> Path:

        file_path = (
            self.directory
            / f"{run.run_id}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                run.to_dict(),
                file,
                indent=2,
                ensure_ascii=False,
            )

        return file_path

    def load(
        self,
        run_id: str,
    ) -> dict:

        file_path = (
            self.directory
            / f"{run_id}.json"
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"Run not found: {run_id}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def list_runs(self) -> list[str]:

        return sorted(
            path.stem
            for path in self.directory.glob(
                "run_*.json"
            )
        )