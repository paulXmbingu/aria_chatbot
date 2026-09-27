INTENT_CATEGORIES = {
    "QUESTION": "The user is asking for a specific fact, answer, or piece of information.",
    "EXPLANATION": "The user wants a concept, topic, or process explained.",
    "INSTRUCTION": "The user is asking how to perform a task or follow a procedure.",
    "CREATION": "The user wants something created, written, designed, or generated.",
    "CODING": "The user is asking for programming, software engineering, or code-related help.",
    "ANALYSIS": "The user wants information examined, interpreted, evaluated, or broken down.",
    "COMPARISON": "The user wants two or more things compared.",
    "TROUBLESHOOTING": "The user is experiencing a problem and wants help identifying or fixing it.",
    "CASUAL_CONVERSATION": "The user is engaging in general conversation without a specific task.",
    "CLARIFICATION": "The user is asking to clarify or refine something previously discussed.",
}


INTENT_DETECTION_PROMPT = """
Determine the primary intent of the user's message.

Choose exactly one intent from the following categories:

{intent_categories}

Rules:

- Select the intent that best represents the user's primary goal.
- Consider the conversation context when determining intent.
- Do not invent an intent outside the provided categories.
- Return only the intent name.
""".strip()