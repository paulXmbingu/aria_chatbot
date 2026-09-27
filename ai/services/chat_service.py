from asgiref.sync import sync_to_async

from ai.memory.memory_manager import MemoryManager
from ai.services.ai_service import AIService
from ai.services.context_prompt_service import (
    ContextPromptService,
)
from ai.services.conversation_context_service import (
    ConversationContextService,
)
from ai.services.conversation_title_service import (
    ConversationTitleService,
)
from ai.services.intent_service import IntentService
from ai.services.response_planning_service import (
    ResponsePlanningService,
)
from apps.chat.models import Conversation, Message


class ChatService:
    @staticmethod
    async def generate_response(
        conversation: Conversation,
        message: str,
    ) -> Message | None:
        intent = await IntentService.detect(
            message
        )

        plan = await ResponsePlanningService.plan(
            message
        )

        user_message = await sync_to_async(
            Message.objects.create
        )(
            conversation=conversation,
            role="user",
            content=message,
        )

        memory_manager = MemoryManager()

        await memory_manager.process(
            message
        )

        context = await ConversationContextService.build(
            conversation=conversation,
            current_message=message,
            intent=intent,
        )

        prompt = ContextPromptService.build(
            context,
            plan=plan,
        )

        response = await AIService.generate(
            prompt
        )

        if not response:
            return None

        assistant_message = await sync_to_async(
            Message.objects.create
        )(
            conversation=conversation,
            role="assistant",
            content=response,
        )

        await ChatService.update_title(
            conversation=conversation,
        )

        return assistant_message

    @staticmethod
    async def update_title(
        conversation: Conversation,
    ) -> None:
        has_title = bool(
            conversation.title.strip()
        )

        if has_title:
            return

        messages = await ConversationContextService.get_messages(
            conversation=conversation,
        )

        if not messages:
            return

        conversation_context = "\n".join(
            ConversationContextService.format_message(
                message
            )
            for message in messages
        )

        title = (
            await ConversationTitleService.generate(
                conversation_context
            )
        )

        if not title:
            return

        conversation.title = title

        await sync_to_async(
            conversation.save
        )(
            update_fields=[
                "title",
            ]
        )

    @staticmethod
    async def regenerate_response(
        conversation: Conversation,
        assistant_message: Message,
    ) -> str:
        user_message = await sync_to_async(
            lambda: Message.objects.filter(
                conversation=conversation,
                created_at__lt=assistant_message.created_at,
                role="user",
            )
            .order_by("-created_at")
            .first()
        )()

        if not user_message:
            raise ValueError(
                "No user message found for regeneration."
            )

        intent = await IntentService.detect(
            user_message.content
        )

        plan = await ResponsePlanningService.plan(
            user_message.content
        )

        context = await ConversationContextService.build(
            conversation=conversation,
            current_message=user_message.content,
            exclude_message=assistant_message,
            include_current=False,
            intent=intent,
        )

        prompt = ContextPromptService.build(
            context,
            plan=plan,
        )

        response = await AIService.generate(
            prompt
        )

        if not response:
            return ""

        assistant_message.content = response

        await sync_to_async(
            assistant_message.save
        )(
            update_fields=[
                "content",
            ]
        )

        return response