from ai.retrieval.knowledge_store import KnowledgeStore
from ai.retrieval.retrieval_result import RetrievalResult


class RetrievalService:
    def __init__(
        self,
        knowledge_store: KnowledgeStore | None = None,
    ) -> None:
        self.knowledge_store = (
            knowledge_store
            or KnowledgeStore()
        )

    async def search(
        self,
        query: str,
    ) -> list[RetrievalResult]:
        if not query.strip():
            return []

        documents = self.knowledge_store.get_all()

        query_terms = set(
            query.lower().split()
        )

        results: list[RetrievalResult] = []

        for document in documents:
            content_terms = set(
                document.content.lower().split()
            )

            score = len(
                query_terms & content_terms
            )

            if score > 0:
                results.append(
                    RetrievalResult(
                        content=document.content,
                        source=document.source,
                        score=float(score),
                    )
                )

        results.sort(
            key=lambda result: (
                result.score or 0
            ),
            reverse=True,
        )

        return results