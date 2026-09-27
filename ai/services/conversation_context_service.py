from asgiref.sync import sync_to_async

from ai.services.context import Context
from apps.chat.models import Conversation, Message


class ConversationContextService:
    MAX_RECENT_MESSAGES = 10

    @staticmethod
    async def get_messages(
        conversation: Conversation,
        exclude_message: Message | None = None,
    ) -> list[Message]:
        def query_messages():
            queryset = Message.objects.filter(
                conversation=conversation,
            ).order_by("created_at")

            if exclude_message is not None:
                queryset = queryset.exclude(
                    pk=exclude_message.pk
                )

            return list(queryset)

        return await sync_to_async(
            query_messages
        )()

    @staticmethod
    def format_message(
        message: Message,
    ) -> str:
        role = (
            "User"
            if message.role == "user"
            else "Assistant"
        )

        return f"{role}: {message.content}"

    @classmethod
    def select_recent_messages(
        cls,
        messages: list[Message],
    ) -> list[str]:
        recent_messages = messages[
            -cls.MAX_RECENT_MESSAGES:
        ]

        return [
            cls.format_message(message)
            for message in recent_messages
        ]

    @classmethod
    async def build(
        cls,
        conversation: Conversation,
        current_message: str | None = None,
        exclude_message: Message | None = None,
        include_current: bool = True,
        intent: str | None = None,
    ) -> Context:
        messages = await cls.get_messages(
            conversation=conversation,
            exclude_message=exclude_message,
        )

        history = [
            cls.format_message(message)
            for message in messages
        ]

        recent_messages = (
            cls.select_recent_messages(
                messages
            )
        )

        return Context(
            conversation_id=conversation.pk,
            history=history,
            recent_messages=recent_messages,
            current_message=(
                current_message
                if include_current
                and current_message is not None
                else ""
            ),
            intent=intent,
        )