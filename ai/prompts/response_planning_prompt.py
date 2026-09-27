RESPONSE_PLANNING_PROMPT = """
Determine how the assistant should respond to the user's message.

Choose exactly one value for each category.

## Response Approach

{response_approaches}

## Response Depth

{response_depths}

## Response Structure

{response_structures}

## Complexity

{complexity_levels}

## Rules

- Choose the approach that best matches the user's primary goal.
- Choose concise depth for simple requests unless more detail is clearly useful.
- Choose moderate or detailed depth when the task requires explanation or multiple steps.
- Choose a structure that makes the response easy to understand.
- Set requires_clarification to true only when essential information is missing.
- Do not ask for clarification when the request can reasonably be completed with the available information.
- Estimate complexity based on the reasoning or task handling required.
- Return only valid JSON.
- Do not include Markdown or additional explanation.

## Required JSON Format

{{
    "approach": "ANSWER",
    "depth": "CONCISE",
    "structure": "PARAGRAPH",
    "requires_clarification": false,
    "complexity": "SIMPLE"
}}

## User Message

{message}
""".strip()