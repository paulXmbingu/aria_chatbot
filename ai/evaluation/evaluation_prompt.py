from ai.evaluation.evaluation_criteria import (
    EVALUATION_CRITERIA,
)


EVALUATION_PROMPT = """
Evaluate the AI response against the provided criteria.

Criteria:

{criteria}

Rules:

- Evaluate only the response provided.
- Do not rewrite the response.
- Do not add explanations outside the required format.
- Return a score from 0.0 to 1.0 for each criterion.
- Return the overall score from 0.0 to 1.0.
- Return only valid JSON.

Expected format:

{{
    "criteria": {{
        "RELEVANCE": 0.0,
        "CLARITY": 0.0,
        "COMPLETENESS": 0.0,
        "ACCURACY": 0.0,
        "INSTRUCTION_FOLLOWING": 0.0
    }},
    "overall_score": 0.0,
    "issues": []
}}

Response:

{response}
""".strip()


def build_evaluation_prompt(
    response: str,
) -> str:
    criteria = "\n".join(
        f"- {name}: {description}"
        for name, description
        in EVALUATION_CRITERIA.items()
    )

    return EVALUATION_PROMPT.format(
        criteria=criteria,
        response=response,
    )