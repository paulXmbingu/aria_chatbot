-- Active: 1790455992930@@127.0.0.1@3306
import os

from ollama import Client


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)


MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b",
)


client = Client(
    host=OLLAMA_HOST
)