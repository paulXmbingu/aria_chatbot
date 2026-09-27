from ai.memory.memory import Memory, MemoryType
from ai.services.ai_service import AIService


MEMORY_EXTRACTION_PROMPT = """
Identify information from the user's message that may be useful
to remember across future conversations.

Memory categories:

- PREFERENCE: A stated user preference.
- USER_FACT: A stable fact about the user.
- PROJECT_CONTEXT: Important information about an ongoing project.
- INSTRUCTION: A persistent instruction about how the assistant should behave.

Rules:

- Only extract information explicitly supported by the user's message.
- Do not infer personal facts.
- Do not store temporary or conversation-specific information.
- Do not store sensitive personal information.
- If there is nothing worth remembering, return NONE.
- Return only one memory.
- Format the response exactly as:

TYPE: <MEMORY_TYPE>
CONTENT: <memory>

User message:
{message}
""".strip()


class MemoryExtractionService:
    @staticmethod
    def build_prompt(
        message: str,
    ) -> str:
        return MEMORY_EXTRACTION_PROMPT.format(
            message=message
        )

    @staticmethod
    def parse(
        response: str | None,
    ) -> Memory | None:
        if not response:
            return None

        normalized = response.strip()

        if normalized.upper() == "NONE":
            return None

        memory_type: MemoryType | None = None
        content: str | None = None

        for line in normalized.splitlines():
            line = line.strip()

            if line.upper().startswith("TYPE:"):
                value = line.split(
                    ":",
                    1,
                )[1].strip().upper()

                try:
                    memory_type = MemoryType(value)
                except ValueError:
                    return None

            elif line.upper().startswith("CONTENT:"):
                content = line.split(
                    ":",
                    1,
                )[1].strip()

        if memory_type is None or not content:
            return None

        return Memory(
            type=memory_type,
            content=content,
        )

    @classmethod
    async def extract(
        cls,
        message: str,
    ) -> Memory | None:
        prompt = cls.build_prompt(
            message
        )

        response = await AIService.generate(
            prompt
        )

        return cls.parse(
            response
        )