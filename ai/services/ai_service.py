from google.adk.runners import InMemoryRunner

from ai.agents.chat_agent import root_agent


class AIService:

    @staticmethod
    async def generate(
        prompt: str,
    ) -> str | None:
        runner = InMemoryRunner(
            agent=root_agent,
        )

        events = await runner.run_debug(
            prompt,
        )

        for event in reversed(events):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        return part.text

        return None