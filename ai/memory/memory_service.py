from ai.memory.memory import Memory, MemoryType
from ai.memory.memory_store import MemoryStore


class MemoryService:
    def __init__(
        self,
        store: MemoryStore | None = None,
    ) -> None:
        self.store = store or MemoryStore()

    @staticmethod
    def create(
        memory_type: MemoryType,
        content: str,
        confidence: float = 1.0,
    ) -> Memory:
        return Memory(
            type=memory_type,
            content=content,
            confidence=confidence,
        )

    @staticmethod
    def is_valid(
        memory: Memory,
    ) -> bool:
        return bool(
            memory.content.strip()
        ) and 0.0 <= memory.confidence <= 1.0

    async def add(
        self,
        memory: Memory,
    ) -> Memory | None:
        if not self.is_valid(memory):
            return None

        return await self.store.add(
            memory
        )

    async def get_all(self) -> list[Memory]:
        return await self.store.get_all()

    async def remove(
        self,
        memory_id: int,
    ) -> None:
        await self.store.remove(
            memory_id
        )

    async def clear(self) -> None:
        await self.store.clear()