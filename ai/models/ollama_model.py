import os

from ollama import Client


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)


MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:12b",
)


client = Client(
    host=OLLAMA_HOST,
)