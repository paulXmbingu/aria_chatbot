from ai.services.response_quality import (
    ResponseQuality,
    ResponseQualityService,
)


class ResponseValidator:
    @staticmethod
    def validate(
        response: str | None,
    ) -> ResponseQuality:
        quality = ResponseQualityService.evaluate(
            response
        )

        if not quality.is_valid:
            return quality

        if not ResponseQualityService.is_acceptable(
            quality
        ):
            return ResponseQuality(
                is_valid=False,
                score=quality.score,
                issues=[
                    *quality.issues,
                    "Response did not meet the quality threshold.",
                ],
            )

        return quality