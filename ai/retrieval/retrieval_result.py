from dataclasses import dataclass


@dataclass
class RetrievalResult:
    content: str
    source: str | None = None
    score: float | None = None