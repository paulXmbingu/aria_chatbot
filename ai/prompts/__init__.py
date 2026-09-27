from ai.prompts.behavior import BEHAVIOR_PROMPT
from ai.prompts.conversation import CONVERSATION_PROMPT
from ai.prompts.identity import IDENTITY_PROMPT
from ai.prompts.response import RESPONSE_PROMPT


SYSTEM_PROMPT = "\n\n".join(
    [
        IDENTITY_PROMPT,
        BEHAVIOR_PROMPT,
        CONVERSATION_PROMPT,
        RESPONSE_PROMPT,
    ]
)