from enum import StrEnum

from ai.reasoning.task_plan import TaskPlan


class TaskState(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskStateService:
    @staticmethod
    def get_state(
        plan: TaskPlan,
    ) -> TaskState:
        if not plan.steps:
            return TaskState.PENDING

        if all(
            step.completed
            for step in plan.steps
        ):
            return TaskState.COMPLETED

        if any(
            step.completed
            for step in plan.steps
        ):
            return TaskState.IN_PROGRESS

        return TaskState.IN_PROGRESS