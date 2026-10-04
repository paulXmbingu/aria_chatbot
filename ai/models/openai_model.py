import os

from openai import OpenAI


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
)


GPT_6_ASTRA = os.getenv(
    "OPENAI_MODEL_GPT_6_ASTRA",
    "gpt-6-astra",
)


GPT_5_6 = os.getenv(
    "OPENAI_MODEL_GPT_5_6",
    "gpt-5.6",
)


client = OpenAI(
    api_key=OPENAI_API_KEY,
)