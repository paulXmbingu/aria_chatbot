REASONING_PROMPT = """
Break the user's request into a small number of logical steps.

Rules:

- Only create steps that are necessary to complete the request.
- Keep each step concise.
- Preserve the user's requirements and constraints.
- Do not solve the task.
- Return only the steps.
- Format each step as:

1. <step>
2. <step>
3. <step>

User request:
{message}
""".strip()


def build_reasoning_prompt(
    message: str,
) -> str:
    return REASONING_PROMPT.format(
        message=message
    )