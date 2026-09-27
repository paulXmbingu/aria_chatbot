from ai.memory.memory import Memory
from ai.memory.memory_extraction_service import (
    MemoryExtractionService,
)
from ai.memory.memory_service import MemoryService


class MemoryManager:
    def __init__(
        self,
        memory_service: MemoryService | None = None,
    ) -> None:
        self.memory_service = (
            memory_service
            or MemoryService()
        )

    async def process(
        self,
        message: str,
    ) -> Memory | None:
        memory = await MemoryExtractionService.extract(
            message
        )

        if memory is None:
            return None

        return await self.memory_service.add(
            memory
        )

    async def get_memories(self) -> list[Memory]:
        return await self.memory_service.get_all()

    async def clear(self) -> None:
        await self.memory_service.clear()