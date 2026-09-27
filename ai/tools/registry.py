from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolDefinition:
    name: str
    description: str
    function: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(
        self,
        tool: ToolDefinition,
    ) -> None:
        self._tools[tool.name] = tool

    def get(
        self,
        name: str,
    ) -> ToolDefinition | None:
        return self._tools.get(name)

    def get_all(self) -> list[ToolDefinition]:
        return list(self._tools.values())

    def has(
        self,
        name: str,
    ) -> bool:
        return name in self._tools