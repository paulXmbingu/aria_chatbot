import json

from ai.prompts.planning import PLANNING_PROMPT
from ai.services.ai_service import AIService
from ai.services.response_plan import (
    COMPLEXITY_LEVELS,
    RESPONSE_APPROACHES,
    RESPONSE_DEPTHS,
    RESPONSE_STRUCTURES,
    ResponsePlan,
)


class ResponsePlanningService:

    @staticmethod
    def build_prompt(
        message: str,
    ) -> str:

        response_approaches = "\n".join(
            f"- {name}: {description}"
            for name, description
            in RESPONSE_APPROACHES.items()
        )

        response_depths = "\n".join(
            f"- {name}: {description}"
            for name, description
            in RESPONSE_DEPTHS.items()
        )

        response_structures = "\n".join(
            f"- {name}: {description}"
            for name, description
            in RESPONSE_STRUCTURES.items()
        )

        complexity_levels = "\n".join(
            f"- {name}: {description}"
            for name, description
            in COMPLEXITY_LEVELS.items()
        )

        return PLANNING_PROMPT.format(
            response_approaches=response_approaches,
            response_depths=response_depths,
            response_structures=response_structures,
            complexity_levels=complexity_levels,
            message=message,
        )

    @staticmethod
    def parse_plan(
        response: str | None,
    ) -> ResponsePlan | None:

        if not response:
            return None

        response = response.strip()

        if response.startswith("```"):
            lines = response.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            response = "\n".join(lines).strip()

        try:
            data = json.loads(response)

        except json.JSONDecodeError:
            return None

        if not isinstance(data, dict):
            return None

        approach = data.get("approach")
        depth = data.get("depth")
        structure = data.get("structure")
        requires_clarification = data.get(
            "requires_clarification"
        )
        complexity = data.get("complexity")

        if approach not in RESPONSE_APPROACHES:
            return None

        if depth not in RESPONSE_DEPTHS:
            return None

        if structure not in RESPONSE_STRUCTURES:
            return None

        if not isinstance(
            requires_clarification,
            bool,
        ):
            return None

        if complexity not in COMPLEXITY_LEVELS:
            return None

        return ResponsePlan(
            approach=approach,
            depth=depth,
            structure=structure,
            requires_clarification=(
                requires_clarification
            ),
            complexity=complexity,
        )

    @staticmethod
    async def plan(
        message: str,
    ) -> ResponsePlan | None:

        prompt = ResponsePlanningService.build_prompt(
            message
        )

        response = await AIService.generate(
            prompt
        )

        return ResponsePlanningService.parse_plan(
            response
        )