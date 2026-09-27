from ai.evaluation.evaluation_result import (
    EvaluationResult,
)


class EvaluationService:
    @staticmethod
    def evaluate(
        response: str | None,
    ) -> EvaluationResult:
        issues: list[str] = []

        if not response or not response.strip():
            issues.append(
                "Response is empty."
            )

        score = 1.0

        if issues:
            score = 0.0

        return EvaluationResult(
            passed=not issues,
            score=score,
            issues=issues,
        )