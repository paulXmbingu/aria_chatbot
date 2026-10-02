from dataclasses import dataclass


RESPONSE_APPROACHES = {
    "ANSWER": "Provide a direct answer.",
    "EXPLAIN": "Explain a concept, topic, or process.",
    "INSTRUCT": "Provide actionable steps or instructions.",
    "CREATE": "Create or generate the requested content.",
    "ANALYZE": "Break down and interpret information.",
    "COMPARE": "Compare multiple subjects or options.",
    "TROUBLESHOOT": "Identify and help resolve a problem.",
    "CLARIFY": "Ask for missing information before proceeding.",
    "CONVERSE": "Respond naturally in a conversational manner.",
}


RESPONSE_DEPTHS = {
    "CONCISE": "Give only the essential information.",
    "MODERATE": (
        "Provide enough explanation to be useful "
        "without excessive detail."
    ),
    "DETAILED": (
        "Provide a thorough explanation with "
        "relevant supporting detail."
    ),
}


RESPONSE_STRUCTURES = {
    "PARAGRAPH": "Use concise paragraphs.",
    "BULLETS": "Use bullet points.",
    "NUMBERED_STEPS": "Use ordered steps.",
    "TABLE": "Use a structured table.",
    "SECTIONS": "Organize the response into sections.",
    "CODE": "Prioritize code with supporting explanation.",
    "MIXED": "Combine appropriate structures.",
}


COMPLEXITY_LEVELS = {
    "SIMPLE": "The request can be handled directly.",
    "MODERATE": (
        "The request requires some reasoning or organization."
    ),
    "COMPLEX": (
        "The request requires multiple reasoning steps "
        "or substantial task handling."
    ),
}


@dataclass
class ResponsePlan:
    approach: str
    depth: str
    structure: str
    requires_clarification: bool
    complexity: str