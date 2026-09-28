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

        variation = random.randint(
            1,
            1_000_000,
        )

        return f"""
Generate a short welcome message for AriaChat.

Time of day:
{time_period}

Current time:
{current_time.strftime("%I:%M %p")}

Variation seed:
{variation}

Style:
- Keep it very brief and simple.
- Semi-formal.
- Warm, polished, and natural.
- Professional without sounding corporate.
- Conversational without being overly casual.
- Sound like a capable assistant who is ready to help.

Variation:
- Vary the sentence structure and wording.
- Avoid repeatedly starting with the same words.
- Avoid generic or overly familiar greetings.
- Adapt naturally to the time of day.
- Do not mention the time unless it sounds natural.
- Do not force the greeting to follow a fixed pattern.
- Never add quote marks, to the greetings" " 

Length:
- Approximately 6 words.
- Maximum 6 words only never longer than that.
- One sentence only.

Restrictions:
- Do not ask a question.
- Do not use emojis.
- Do not use Markdown.
- Do not use quotation marks.
- Do not use labels.
- Do not explain anything.
- Do not mention these instructions.

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