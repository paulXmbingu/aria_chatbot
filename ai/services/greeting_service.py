from datetime import datetime
import random

from ai.services.ai_service import AIService


class GreetingService:

    @staticmethod
    def build_prompt(
        current_time: datetime,
    ) -> str:

        hour = current_time.hour

        if 5 <= hour < 12:
            time_period = "morning"
        elif 12 <= hour < 18:
            time_period = "afternoon"
        elif 18 <= hour < 23:
            time_period = "evening"
        else:
            time_period = "late night"

        variation = random.randint(1, 1000000)

        return f"""
Generate a short welcome message for Aria Chat.

Time of day: {time_period}
Variation seed: {variation}

Return ONLY the welcome message.

Rules:
- 4 to 6 words.
- One sentence only.
- Natural and conversational.
- Make Aria sound ready to help.
- Vary the wording every time.
- Avoid common repeated phrases.
- Do not explain anything.
- No Markdown.
- No quotation marks.
- No emojis.
- No questions.
- No labels.
- No additional text.

Return only the final greeting.
""".strip()

    @staticmethod
    async def generate(
        current_time: datetime,
    ) -> str | None:

        prompt = GreetingService.build_prompt(
            current_time
        )

        response = await AIService.generate(
            prompt
        )

        if not response:
            return None

        return response.strip().splitlines()[0]