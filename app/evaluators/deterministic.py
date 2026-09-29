import re

from app.evaluation_result import EvaluationResult


class DeterministicEvaluator:

    # Does this exact piece of text occur?
    def contains(
        self,
        text: str,
        expected: str,
    ) -> EvaluationResult:      
        """
        Check whether the expected text exists inside the actual text.
        Case-insensitive.
        """

        passed = expected.lower() in text.lower()

        return EvaluationResult(
           evaluator="deterministic",
           criterion="contains",
           score=1.0 if passed else 0.0,
           passed=passed,
           reason=(
                "Expected text was found in the answer."
                if passed
                else "Expected text was not found in the answer."
            ),
           metadata={
               "expected": expected,
           }
        )

    # Does this text follow a particular pattern?
    def regex(
        self,
        text: str,
        pattern: str,
    ) -> EvaluationResult:
        """
        Check whether the text matches a regular expression.
        """

        passed = bool(
            re.search(
                pattern,
                text,
                re.IGNORECASE,
            )
        )

        return EvaluationResult(
            evaluator="deterministic",
            criterion="regex",
            score=1.0 if passed else 0.0,
            passed=passed,
            reason=(
                "Answer matches the required pattern."
                if passed
                else "Answer does not match the required pattern."
            ),
            metadata={
                "pattern": pattern,
            },
        )

    # Is the answer no longer than x characters?
    def max_length(
        self,
        text: str,
        maximum: int,
    ) -> EvaluationResult:
        """
        Check whether text length is within the maximum limit.
        """

        actual_length = len(text)

        passed = actual_length <= maximum

        return EvaluationResult(
            evaluator="deterministic",
            criterion="max_length",
            score=1.0 if passed else 0.0,
            passed=passed,
            reason=(
                "Answer is within the maximum length."
                if passed
                else "Answer exceeds the maximum length."
            ),
            metadata={
                "actual_length": actual_length,
                "maximum": maximum,
            },
        )

    # Is the answer at least 5 characters?
    def min_length(
        self,
        text: str,
        minimum: int,
    ) -> EvaluationResult:
        """
        Check whether text length meets the minimum limit.
        """

        actual_length = len(text)

        passed = actual_length >= minimum

        return EvaluationResult(
            evaluator="deterministic",
            criterion="min_length",
            score=1.0 if passed else 0.0,
            passed=passed,
            reason=(
                "Answer meets the minimum length."
                if passed
                else "Answer is shorter than the minimum length."
            ),
            metadata={
                "actual_length": actual_length,
                "minimum": minimum,
            },
        )