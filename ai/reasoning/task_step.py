from dataclasses import dataclass


@dataclass
class TaskStep:
    order: int
    description: str
    completed: bool = False