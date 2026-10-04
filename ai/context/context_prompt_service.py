from ai.context.context import Context
from ai.planning.response_plan import ResponsePlan


class ContextPromptService:
    @staticmethod
    def build(
        context: Context,
        plan: ResponsePlan | None = None,
    ) -> str:
        history = "\n\n".join(
            context.recent_messages
        )

        intent = (
            context.intent
            if context.intent
            else "UNKNOWN"
        )

        response_plan = ""

        if plan is not None:
            response_plan = (
                "Response plan:\n"
                f"- Approach: {plan.approach}\n"
                f"- Depth: {plan.depth}\n"
                f"- Structure: {plan.structure}\n"
                f"- Complexity: {plan.complexity}\n"
                f"- Requires clarification: "
                f"{plan.requires_clarification}\n\n"
            )

        memories = ""

        if context.memories:
            formatted_memories = "\n".join(
                f"- {memory}"
                for memory in context.memories
            )

            memories = (
                "Relevant user memories:\n"
                f"{formatted_memories}\n\n"
            )

        return (
            f"User intent: {intent}\n\n"
            f"{response_plan}"
            f"{memories}"
            f"Conversation context:\n"
            f"{history}\n\n"
            f"Current user message:\n"
            f"{context.current_message}"
        )