from dataclasses import dataclass


@dataclass
class EvaluationResult:
    passed: bool
    score: float
    issues: list[str]