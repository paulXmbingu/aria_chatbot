import json

from ai.evaluation.evaluation_result import EvaluationResult


class EvaluationParser:
    @staticmethod
    def parse(
        response: str | None,
    ) -> EvaluationResult | None:
        if not response:
            return None

        try:
            data = json.loads(
                response.strip()
            )
        except json.JSONDecodeError:
            return None

        if not isinstance(data, dict):
            return None

        overall_score = data.get(
            "overall_score"
        )

        issues = data.get(
            "issues",
            [],
        )

        if not isinstance(
            overall_score,
            (int, float),
        ):
            return None

        if not isinstance(
            issues,
            list,
        ):
            return None

        score = max(
            0.0,
            min(
                1.0,
                float(overall_score),
            ),
        )

        return EvaluationResult(
            passed=score >= 0.8,
            score=score,
            issues=[
                str(issue)
                for issue in issues
            ],
        )