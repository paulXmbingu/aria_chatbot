from dataclasses import dataclass


@dataclass
class Context:
    conversation_id: int
    history: list[str]
    recent_messages: list[str]
    current_message: str
    intent: str | None = None