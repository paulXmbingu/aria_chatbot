from dataclasses import dataclass
from enum import StrEnum


class MemoryType(StrEnum):
    PREFERENCE = "PREFERENCE"
    USER_FACT = "USER_FACT"
    PROJECT_CONTEXT = "PROJECT_CONTEXT"
    INSTRUCTION = "INSTRUCTION"


@dataclass
class Memory:
    type: MemoryType
    content: str
    confidence: float = 1.0