from asgiref.sync import sync_to_async

from ai.memory.memory import Memory, MemoryType
from apps.chat.models import Memory as MemoryModel


class MemoryStore:
    @staticmethod
    async def add(
        memory: Memory,
    ) -> Memory:
        model = await sync_to_async(
            MemoryModel.objects.create
        )(
            type=memory.type.value,
            content=memory.content,
            confidence=memory.confidence,
        )

        return Memory(
            type=MemoryType(model.type),
            content=model.content,
            confidence=model.confidence,
        )

    @staticmethod
    async def get_all() -> list[Memory]:
        models = await sync_to_async(
            lambda: list(
                MemoryModel.objects.all()
            )
        )()

        return [
            Memory(
                type=MemoryType(model.type),
                content=model.content,
                confidence=model.confidence,
            )
            for model in models
        ]

    @staticmethod
    async def remove(
        memory_id: int,
    ) -> None:
        await sync_to_async(
            MemoryModel.objects.filter(
                id=memory_id
            ).delete
        )()

    @staticmethod
    async def clear() -> None:
        await sync_to_async(
            MemoryModel.objects.all().delete
        )()