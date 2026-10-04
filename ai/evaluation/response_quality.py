from dataclasses import dataclass


@dataclass
class ResponseQuality:
    is_valid: bool
    score: float
    issues: list[str]


class ResponseQualityService:
    MIN_RESPONSE_LENGTH = 2

    @staticmethod
    def evaluate(
        response: str | None,
    ) -> ResponseQuality:
        if not response or not response.strip():
            return ResponseQuality(
                is_valid=False,
                score=0.0,
                issues=[
                    "Response is empty."
                ],
            )

        issues: list[str] = []

        normalized = response.strip()

        if len(normalized) < (
            ResponseQualityService.MIN_RESPONSE_LENGTH
        ):
            issues.append(
                "Response is too short."
            )

        score = 1.0

        if issues:
            score = max(
                0.0,
                score - (
                    0.2 * len(issues)
                ),
            )

        return ResponseQuality(
            is_valid=not issues,
            score=score,
            issues=issues,
        )

    @staticmethod
    def is_acceptable(
        quality: ResponseQuality,
    ) -> bool:
        return (
            quality.is_valid
            and quality.score >= 0.8
        )