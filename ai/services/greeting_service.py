from datetime import datetime

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

        return f"""
You are generating the welcome text displayed on the Aria Chat home screen.

Time of day: {time_period}

Return ONLY the welcome message.

STRICT RULES:
- One sentence only.
- 4 to 8 words.
- Friendly and natural.
- Make it clear that Aria is ready to help.
- Keep it concise.
- No explanations.
- No introduction.
- No labels.
- No Markdown.
- No quotation marks.
- No emojis.
- No questions.
- Do not say "Here is".
- Do not say "welcome message".
- Do not provide examples.
- Do not provide additional text.

Good examples:
Good morning, ready to help.
Good afternoon, ready to help.
Good evening, ready to help.
I'm ready to help.
Ready to help you get started.

Return ONLY the final sentence.
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