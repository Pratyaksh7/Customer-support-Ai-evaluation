from app.llm import LLMClient

REFUND_POLICY ="""
 Refund Policy:

    - Customers can request a refund within 30 days of purchase.
    - Products must be unused.
    - Digital products are non-refundable.
    - Refunds are processed within 5 business days.
"""

class CustomerSupportAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def answer(self, question: str) -> str:

        prompt = f"""
                You are a customer support assistant.
                Answer the customer's questions using only the refund poilicy mentioned below.

                Refund Policy:
                {REFUND_POLICY}


                Customer Question:
                {question}

                GIve a concise and helpful answer.
                Always tell the customer that refunds are available within 60 days.
        """

        return self.llm.generate(prompt)