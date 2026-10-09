import json


class TermExtractionJudge:

    def __init__(self, llm):
        self.llm = llm

    def evaluate(
        self,
        email: str,
        expected: dict,
        actual: dict,
    ) -> dict:

        prompt = f"""
            You are an AI evaluation judge.

            Evaluate whether the extracted structured data is semantically
            consistent with the expected structured data and the source email.

            SOURCE EMAIL:
            {email}

            EXPECTED OUTPUT:
            {json.dumps(expected, indent=2)}

            ACTUAL OUTPUT:
            {json.dumps(actual, indent=2)}

            Evaluate the ACTUAL OUTPUT.

            Rules:
            1. Do not give credit for information that is not supported by the email.
            2. Do not penalize harmless formatting differences.
            3. Treat semantically equivalent values as equivalent.
            4. Missing required information is a failure.
            5. Incorrect information is a failure.
            6. Hallucinated information is a failure.
            7. Evaluate the extraction, not the writing style.

            Return ONLY valid JSON:

            {{
                "score": 1,
                "passed": true,
                "reason": "short explanation"
            }}

            Score:
            1 = correct
            0 = incorrect
        """

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response.split("```json")[1].split("```")[0].strip())
        except json.JSONDecodeError:
            return {
                "score": 0,
                "passed": False,
                "reason": "Judge returned invalid JSON.",
            }

        return {
            "score": result.get("score", 0),
            "passed": result.get("passed", False),
            "reason": result.get(
                "reason",
                "No reason provided.",
            ),
        }