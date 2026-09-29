import os

import litellm
from litellm import completion

from dotenv import load_dotenv
from ollama import Client



load_dotenv()


class LLMClient:
    def __init__(self):
        self.model = os.environ.get(
            "LLM_MODEL", "ollama/gemma4:31b-cloud"
        )

        self.api_base = os.environ.get(
            "LLM_API_BASE", "http://localhost:11434"
        )

        # The listener runs the pipeline under a lock, so a hung model would
        # stall every queued email, not just this one.
        self.timeout = float(
            os.environ.get("LLM_TIMEOUT_SECONDS", "120")
        )

    def generate(self, prompt: str) -> str:
        response = completion(
            model=self.model,
            api_base = self.api_base,
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            timeout=self.timeout,
        )

        return response.choices[0].message.content