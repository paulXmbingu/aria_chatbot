import logging

from ai.services.ai_service import AIService


logger = logging.getLogger(__name__)


TITLE_PROMPT = """
Analyze the conversation and create a short semantic title.

First identify:

SUBJECT:
The main thing the user is talking about.

GOAL:
What the user wants to do with that subject.

Then combine them into a concise title.

Rules:

- The title must represent the SUBJECT and GOAL.
- Do NOT copy the user's sentence.
- Do NOT use the first words of the user's message.
- Ignore conversational filler.
- Use 3 to 6 words.
- Start with a capital letter.
- Do not use quotation marks.
- Do not use Markdown.
- Do not end with punctuation.

Required format:

SUBJECT: <subject>
GOAL: <goal>
TITLE: <semantic title>

Example:

User message:
I would like to plan a trip to Mars help me prepare

SUBJECT: Mars trip
GOAL: Planning
TITLE: Trip to Mars Planning

Example:

User message:
Can you help me figure out how to deploy my Django AI chatbot?

SUBJECT: Django AI chatbot
GOAL: Deployment
TITLE: Django AI Deployment

Example:

User message:
What is the difference between uv and pipenv?

SUBJECT: UV and Pipenv
GOAL: Comparison
TITLE: UV vs Pipenv

Example:

User message:
Why is PostgreSQL not starting?

SUBJECT: PostgreSQL
GOAL: Troubleshooting
TITLE: PostgreSQL Startup Issue

Now analyze this conversation:

{conversation}
""".strip()


class ConversationTitleService:

    @staticmethod
    def build_prompt(
        conversation: str,
    ) -> str:
        return TITLE_PROMPT.format(
            conversation=conversation
        )

    @staticmethod
    def parse_title(
        response: str | None,
    ) -> str | None:

        if not response:
            logger.warning(
                "Title generation returned no response."
            )
            return None

        response = response.strip()

        logger.info(
            "Raw title response: %r",
            response,
        )

        title = None

        for line in response.splitlines():
            line = line.strip()

            if line.upper().startswith("TITLE:"):
                title = line[6:].strip()
                break

        if not title:
            logger.warning(
                "No TITLE field found in response."
            )
            return None

        title = title.strip("\"'")
        title = " ".join(title.split())
        title = title.rstrip(".!?;:,-")

        if not title:
            logger.warning(
                "Title became empty after parsing."
            )
            return None

        title = title[0].upper() + title[1:]

        if len(title) > 120:
            title = title[:120].rstrip()

        logger.info(
            "Parsed conversation title: %r",
            title,
        )

        return title

    @staticmethod
    async def generate(
        conversation: str,
    ) -> str | None:

        prompt = (
            ConversationTitleService.build_prompt(
                conversation
            )
        )

        logger.info(
            "Generating conversation title..."
        )

        response = await AIService.generate(
            prompt
        )

        return (
            ConversationTitleService.parse_title(
                response
            )
            or "New Conversation"
        )