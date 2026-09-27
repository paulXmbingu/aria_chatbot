from ai.reasoning.task_plan import TaskPlan


class ReasoningService:
    @staticmethod
    def create_plan(
        goal: str,
        steps: list[str],
    ) -> TaskPlan:
        plan = TaskPlan(
            goal=goal
        )

        for description in steps:
            plan.add_step(
                description
            )

        return plan

    @staticmethod
    def complete_step(
        plan: TaskPlan,
        order: int,
    ) -> TaskPlan:
        plan.complete_step(
            order
        )

        return plan