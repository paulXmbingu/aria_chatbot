from ai.memory.memory import Memory
from ai.memory.memory_manager import MemoryManager


class MemoryContextService:
    def __init__(
        self,
        memory_manager: MemoryManager | None = None,
    ) -> None:
        self.memory_manager = (
            memory_manager
            or MemoryManager()
        )

    async def get_memories(self) -> list[Memory]:
        return await self.memory_manager.get_memories()

    @staticmethod
    def format_memories(
        memories: list[Memory],
    ) -> list[str]:
        return [
            memory.content
            for memory in memories
        ]

    async def build(self) -> list[str]:
        memories = await self.get_memories()

        if not memories:
            return []

        return self.format_memories(
            memories
        )