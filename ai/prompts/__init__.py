from ai.prompts.behavior import BEHAVIOR_PROMPT
from ai.prompts.conversation import CONVERSATION_PROMPT
from ai.prompts.context import CONTEXT_PROMPT
from ai.prompts.identity import IDENTITY_PROMPT
from ai.prompts.memory import MEMORY_PROMPT
from ai.prompts.response import RESPONSE_PROMPT
from ai.prompts.safety import SAFETY_PROMPT
from ai.prompts.tools import TOOLS_PROMPT


SYSTEM_PROMPT = "\n\n".join(
    [
        IDENTITY_PROMPT,
        BEHAVIOR_PROMPT,
        CONVERSATION_PROMPT,
        CONTEXT_PROMPT,
        MEMORY_PROMPT,
        SAFETY_PROMPT,
        TOOLS_PROMPT,
        RESPONSE_PROMPT,
    ]
)