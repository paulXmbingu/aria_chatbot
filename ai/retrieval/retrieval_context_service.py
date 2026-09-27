from ai.retrieval.retrieval_result import RetrievalResult


class RetrievalContextService:
    @staticmethod
    def format_results(
        results: list[RetrievalResult],
    ) -> list[str]:
        formatted: list[str] = []

        for result in results:
            source = (
                f"Source: {result.source}\n"
                if result.source
                else ""
            )

            formatted.append(
                f"{source}{result.content}"
            )

        return formatted

    async def build(
        self,
        results: list[RetrievalResult],
    ) -> list[str]:
        if not results:
            return []

        return self.format_results(
            results
        )