import logging

from ai.services.ai_service import AIService


logger = logging.getLogger(__name__)


TITLE_PROMPT = """
Generate a short, meaningful title for this conversation.

The title should describe the user's main topic, goal,
or task based on the conversation.

Rules:

- Use 3 to 6 words.
- Capture the main topic or goal.
- Consider the entire provided conversation context.
- Do not simply copy the user's message.
- Prefer specific wording over generic wording.
- Do not use quotation marks.
- Do not use Markdown.
- Do not include punctuation at the end.
- Do not use phrases such as "User asks", "Help with",
  or "Conversation about".
- Return only the title.

Conversation:

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

        title = response.strip()

        logger.info(
            "Raw title response: %r",
            title,
        )

        title = title.strip(
            "\"'"
        )

        title = " ".join(
            title.split()
        )

        if not title:
            logger.warning(
                "Title response became empty after parsing."
            )
            return None

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

        return ConversationTitleService.parse_title(
            response
        )