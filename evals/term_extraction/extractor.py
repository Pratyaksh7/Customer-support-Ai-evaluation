import json

from evals.term_extraction.prompt import build_prompt

class TermExtractor:

    def __init__(self, llm):
        self.llm = llm

    def extract(self, email, checklist) -> dict:
        prompt = build_prompt(email, checklist)

        response = self.llm.generate(prompt)

        return json.loads(response.split("```json")[1].split("```")[0].strip())