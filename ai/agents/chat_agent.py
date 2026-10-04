import os

from google.adk.agents import Agent

from ai.prompts import SYSTEM_PROMPT


MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:4b" ,
)


root_agent = Agent(
    name="aria_chat_agent",
    model=f"ollama/{MODEL_NAME}",
    description="A conversational AI agent.",
    instruction=SYSTEM_PROMPT,
)