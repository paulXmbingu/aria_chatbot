class ResponseSanitizer:
    @staticmethod
    def sanitize(
        response: str | None,
    ) -> str:
        if not response:
            return ""

        return response.strip()