from ai.services.context import Context


class ContextPromptService:
    @staticmethod
    def build(
        context: Context,
    ) -> str:
        history = "\n\n".join(
            context.recent_messages
        )

        intent = (
            context.intent
            if context.intent
            else "UNKNOWN"
        )

        return (
            f"User intent: {intent}\n\n"
            f"Conversation context:\n"
            f"{history}\n\n"
            f"Current user message:\n"
            f"{context.current_message}"
        )