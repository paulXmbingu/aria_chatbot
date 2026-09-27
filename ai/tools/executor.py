from typing import Any

from ai.tools.registry import ToolRegistry


class ToolExecutor:
    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self.registry = registry

    def execute(
        self,
        name: str,
        arguments: dict[str, Any] | None = None,
    ) -> Any:
        tool = self.registry.get(name)

        if tool is None:
            raise ValueError(
                f"Tool '{name}' is not registered."
            )

        arguments = arguments or {}

        return tool.function(
            **arguments
        )