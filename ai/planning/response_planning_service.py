import json

from ai.planning.response_plan import (
    COMPLEXITY_LEVELS,
    RESPONSE_APPROACHES,
    RESPONSE_DEPTHS,
    RESPONSE_STRUCTURES,
    ResponsePlan,
)
from ai.prompts.planning import PLANNING_PROMPT


class ResponsePlanningService:

    @staticmethod
    def build_prompt(
        message: str,
    ) -> str:
        return PLANNING_PROMPT.format(
            message=message,
            response_approaches=RESPONSE_APPROACHES,
            response_depths=RESPONSE_DEPTHS,
            response_structures=RESPONSE_STRUCTURES,
            complexity_levels=COMPLEXITY_LEVELS,
        )

    @staticmethod
    def parse_plan(
        response: str,
    ) -> ResponsePlan | None:

        try:
            data = json.loads(response)

        except (json.JSONDecodeError, TypeError):
            return None

        required_fields = {
            "approach",
            "depth",
            "structure",
            "requires_clarification",
            "complexity",
        }

        if not required_fields.issubset(data):
            return None

        if data["approach"] not in RESPONSE_APPROACHES:
            return None

        if data["depth"] not in RESPONSE_DEPTHS:
            return None

        if data["structure"] not in RESPONSE_STRUCTURES:
            return None

        if data["complexity"] not in COMPLEXITY_LEVELS:
            return None

        if not isinstance(
            data["requires_clarification"],
            bool,
        ):
            return None

        return ResponsePlan(
            approach=data["approach"],
            depth=data["depth"],
            structure=data["structure"],
            requires_clarification=data["requires_clarification"],
            complexity=data["complexity"],
        )