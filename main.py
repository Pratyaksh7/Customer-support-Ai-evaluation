import json

from app.customer_support import CustomerSupportAgent
from app.evaluator import AnswerEvaluator
from app.llm import LLMClient

def load_evaluation_cases():
    with open("data/evaluation_cases.json", "r") as file:
        return json.load(file)


def main():
    llm = LLMClient()
    agent = CustomerSupportAgent(llm)
    evaluator = AnswerEvaluator(llm)

    cases = load_evaluation_cases()

    for case in cases:
        print("="*80)
        print(f"CASE: {case['id']}")
        print(f"QUESTION: {case['question']}")
        print()

        answer = agent.answer(case['question'])

        print(f"AI ANSWER:")
        print(answer)

        print()
        print("EXPECTED FACTS:")
        print(case["expected_facts"])

        evaluation = evaluator.evaluate(
            question=case['question'],
            ai_answer=answer,
            source_of_truth=case['source_of_truth'],
            expected_facts=case["expected_facts"],
        )

        print()
        print("EVALUATION:")
        
        for criterion, result in evaluation.items():
            print(
                f"{criterion.upper()}: "
                f"{result['score']}/5"
            )
            print(f"Reason: {result['reason']}")
            print()


if __name__ == "__main__":
    main()