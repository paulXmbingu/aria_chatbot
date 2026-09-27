from ai.retrieval.retrieval_result import RetrievalResult


class KnowledgeStore:
    def __init__(self) -> None:
        self._documents: list[RetrievalResult] = []

    def add(
        self,
        content: str,
        source: str | None = None,
    ) -> None:
        self._documents.append(
            RetrievalResult(
                content=content,
                source=source,
            )
        )

    def get_all(self) -> list[RetrievalResult]:
        return list(self._documents)

    def clear(self) -> None:
        self._documents.clear()