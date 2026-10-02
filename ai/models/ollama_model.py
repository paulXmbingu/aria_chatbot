import os

from ollama import Client


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)


MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:4b",
    # "gemma3:12b",
    # "gemma3:27b",
    # "gemma4:e4b",
)


client = Client(
    host=OLLAMA_HOST,
)