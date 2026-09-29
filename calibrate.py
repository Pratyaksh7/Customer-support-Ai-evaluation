#Evaluating the Judge

from app.evaluator import AnswerEvaluator
from app.evaluator_calibration import EvaluatorCalibration
from app.llm import LLMClient


def main():
    llm = LLMClient()

    evaluator = AnswerEvaluator(llm)

    calibration = EvaluatorCalibration(evaluator)

    calibration.run()


if __name__ == "__main__":
    main()