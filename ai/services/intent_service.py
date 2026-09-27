from ai.prompts.intents import (
    INTENT_CATEGORIES,
    INTENT_DETECTION_PROMPT,
)
from ai.services.ai_service import AIService


class IntentService:
    @staticmethod
    def build_prompt(message: str) -> str:
        intent_categories = "\n".join(
            f"- {name}: {description}"
            for name, description in INTENT_CATEGORIES.items()
        )

        return (
            INTENT_DETECTION_PROMPT
            .format(
                intent_categories=intent_categories,
            )
            + f"\n\nUser message:\n{message}"
        )

    @staticmethod
    def parse_intent(
        response: str | None,
    ) -> str | None:
        if not response:
            return None

        normalized = response.strip().upper()

        for intent in INTENT_CATEGORIES:
            if normalized == intent:
                return intent

        for intent in INTENT_CATEGORIES:
            if intent in normalized:
                return intent

        return None

    @staticmethod
    async def detect(
        message: str,
    ) -> str | None:
        prompt = IntentService.build_prompt(
            message
        )

        response = await AIService.generate(
            prompt
        )

        return IntentService.parse_intent(
            response
        )