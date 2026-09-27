from dataclasses import dataclass, field

from ai.reasoning.task_step import TaskStep


@dataclass
class TaskPlan:
    goal: str
    steps: list[TaskStep] = field(
        default_factory=list
    )

    def add_step(
        self,
        description: str,
    ) -> TaskStep:
        step = TaskStep(
            order=len(self.steps) + 1,
            description=description,
        )

        self.steps.append(step)

        return step

    def complete_step(
        self,
        order: int,
    ) -> None:
        for step in self.steps:
            if step.order == order:
                step.completed = True
                return