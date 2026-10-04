import os

from google.adk.agents import Agent

from ai.prompts import SYSTEM_PROMPT


MODEL_PROVIDER = os.getenv(
    "MODEL_PROVIDER",
    "ollama",
)


if MODEL_PROVIDER == "ollama":
    MODEL_NAME = os.getenv(
        "OLLAMA_MODEL",
        "gemma3:4b",
    )

    MODEL = f"ollama/{MODEL_NAME}"

else:
    MODEL_NAME = os.getenv(
        "OPENAI_MODEL_GPT_6_ASTRA",
        "gpt-6-astra",
    )

    MODEL = MODEL_NAME


root_agent = Agent(
    name="aria_chat_agent",
    model=MODEL,
    description="A conversational AI agent.",
    instruction=SYSTEM_PROMPT,
)