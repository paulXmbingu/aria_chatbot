from ai.services.response_quality import (
    ResponseQuality,
    ResponseQualityService,
)
from ai.services.response_sanitizer import (
    ResponseSanitizer,
)
from ai.services.response_validator import (
    ResponseValidator,
)


class ResponseQualityPipeline:
    @staticmethod
    def process(
        response: str | None,
    ) -> tuple[str, ResponseQuality]:
        sanitized = ResponseSanitizer.sanitize(
            response
        )

        quality = ResponseValidator.validate(
            sanitized
        )

        return sanitized, quality