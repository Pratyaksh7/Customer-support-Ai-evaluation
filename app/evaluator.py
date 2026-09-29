import json

from app.llm import LLMClient


class AnswerEvaluator:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.criteria = self._load_criteria()

    def _load_criteria(self):
        with open("config/evaluation_criteria.json", "r") as file:
            config = json.load(file)

        return config


    def evaluate(
        self,
        question: str,
        ai_answer: str,
        source_of_truth: str,
        expected_facts: list[str],
    ) -> dict:

        criteria_text = "\n".join(
            f"{index + 1}. {criterion['name']}: "
            f"{criterion['description']}"
            for index, criterion
            in enumerate(self.criteria["criteria"])
        )

        prompt = f"""
            You are an AI evaluation system.

            Evaluate the AI-generated answer using the evaluation criteria below.

            EVALUATION CRITERIA:

            {criteria_text}

            SCORING

            Use a score from 1 to 5:

            1 = Very poor
            2 = Poor
            3 = Acceptable
            4 = Good
            5 = Excellent

            SOURCE OF TRUTH:

            {source_of_truth}

            CUSTOMER QUESTION:
            {question}

            EXPECTED FACTS:

            {json.dumps(expected_facts, indent=2)}

            AI ANSWER:
            {ai_answer}

            Evaluate the AI answer against the source of truth,
            expected facts, and customer question.

            Important evaluation rules:

            - Do not require the AI answer to use the same wording
            as the expected facts.
            - Evaluate meaning rather than exact text matching.
            - Do not give a high relevance score merely because the
            answer mentions the customer's topic.
            - Information that is unrelated to the user's actual
            question should reduce relevance.
            - Unnecessary information should reduce conciseness.
            - A factually incorrect additional statement should reduce
            correctness and groundedness.
            - Missing an expected fact should reduce completeness.

            Return ONLY valid JSON.

            The JSON must contain one object for every evaluation criterion.

            Format:

            {{
                "criterion_name": {{
                    "score": 1,
                    "reason": "..."
                }}
            }}
            """

        response = self.llm.generate(prompt)

        try:
            return json.loads(response.split("```json")[1].split("```")[0].strip())
        except json.JSONDecodeError:
            raise ValueError(
                f"Evaluator returned invalid JSON:\n{response}"
            )