from ai.tools.registry import ToolDefinition, ToolRegistry


class ToolSelector:
    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self.registry = registry

    def get_tool(
        self,
        name: str,
    ) -> ToolDefinition | None:
        return self.registry.get(name)

    def get_available_tools(
        self,
    ) -> list[ToolDefinition]:
        return self.registry.get_all()

    def has_tool(
        self,
        name: str,
    ) -> bool:
        return self.registry.has(name)

    def select(
        self,
        message: str,
    ) -> list[ToolDefinition]:
        message_lower = message.lower()

        selected: list[ToolDefinition] = []

        for tool in self.registry.get_all():
            keywords = tool.description.lower().split()

            if any(
                keyword in message_lower
                for keyword in keywords
                if len(keyword) > 3
            ):
                selected.append(tool)

        return selected