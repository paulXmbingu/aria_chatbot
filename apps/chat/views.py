import logging

from typing import Any, cast

from asgiref.sync import async_to_sync

from django.db.models import Prefetch

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.services.chat_service import ChatService

from .models import Conversation, Message
from .serializers import (
    ChatMessageSerializer,
    ConversationSerializer,
    RegenerateMessageSerializer,
    RenameConversationSerializer,
)


logger = logging.getLogger(__name__)


class ConversationListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ConversationSerializer

    def get_queryset(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        return (
            Conversation.objects
            .prefetch_related(
                Prefetch(
                    "messages",
                    queryset=Message.objects.order_by(
                        "created_at"
                    ),
                )
            )
            .order_by("-created_at")
        )


class ChatMessageView(APIView):
    def post(self, request):
        serializer = ChatMessageSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        data = cast(
            dict[str, Any],
            serializer.validated_data,
        )

        conversation_id = data["conversation_id"]
        message = data["message"]

        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )
        except Conversation.DoesNotExist:
            logger.warning(
                "Conversation %s not found",
                conversation_id,
            )

            return Response(
                {
                    "error": "Conversation not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            assistant_message = async_to_sync(
                ChatService.generate_response
            )(
                conversation,
                message,
            )
        except Exception:
            logger.exception(
                "Failed to generate chat response "
                "for conversation %s",
                conversation_id,
            )

            return Response(
                {
                    "error": (
                        "Unable to generate a response "
                        "right now."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if assistant_message is None:
            logger.error(
                "No assistant response generated "
                "for conversation %s",
                conversation_id,
            )

            return Response(
                {
                    "error": (
                        "Unable to generate a response "
                        "right now."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "message_id": cast(
                    int,
                    assistant_message.pk,
                ),
                "response": cast(
                    str,
                    assistant_message.content,
                ),
            },
            status=status.HTTP_200_OK,
        )


class RegenerateMessageView(APIView):
    def post(self, request):
        serializer = RegenerateMessageSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        data = cast(
            dict[str, Any],
            serializer.validated_data,
        )

        conversation_id = data["conversation_id"]
        message_id = data["message_id"]

        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )
        except Conversation.DoesNotExist:
            logger.warning(
                "Conversation %s not found",
                conversation_id,
            )

            return Response(
                {
                    "error": "Conversation not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            assistant_message = Message.objects.get(
                id=message_id,
                conversation=conversation,
                role="assistant",
            )
        except Message.DoesNotExist:
            logger.warning(
                "Assistant message %s not found "
                "in conversation %s",
                message_id,
                conversation_id,
            )

            return Response(
                {
                    "error": "Assistant message not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            response = async_to_sync(
                ChatService.regenerate_response
            )(
                conversation,
                assistant_message,
            )
        except ValueError as error:
            logger.warning(
                "Unable to regenerate message %s: %s",
                message_id,
                error,
            )

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception(
                "Failed to regenerate message %s "
                "for conversation %s",
                message_id,
                conversation_id,
            )

            return Response(
                {
                    "error": (
                        "Unable to generate the "
                        "response right now."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "message_id": cast(
                    int,
                    assistant_message.pk,
                ),
                "response": response,
            },
            status=status.HTTP_200_OK,
        )


class RenameConversationView(APIView):
    def patch(
        self,
        request,
        conversation_id,
    ):
        serializer = RenameConversationSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        data = cast(
            dict[str, Any],
            serializer.validated_data,
        )

        title = data["title"]

        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )
        except Conversation.DoesNotExist:
            logger.warning(
                "Conversation %s not found for rename",
                conversation_id,
            )

            return Response(
                {
                    "error": "Conversation not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        conversation.title = title
        conversation.save(
            update_fields=["title"]
        )

        return Response(
            {
                "id": conversation.pk,
                "title": conversation.title,
            },
            status=status.HTTP_200_OK,
        )


class DeleteConversationView(APIView):
    def delete(
        self,
        request,
        conversation_id,
    ):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )
        except Conversation.DoesNotExist:
            logger.warning(
                "Conversation %s not found for deletion",
                conversation_id,
            )

            return Response(
                {
                    "error": "Conversation not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        conversation.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class GreetingView(APIView):
    def get(self, request):
        from datetime import datetime

        from ai.services.greeting_service import (
            GreetingService,
        )

        try:
            greeting = async_to_sync(
                GreetingService.generate
            )(
                datetime.now(),
            )
        except Exception:
            logger.exception(
                "Failed to generate greeting"
            )

            return Response(
                {
                    "error": (
                        "Unable to generate greeting."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if not greeting:
            logger.error(
                "Greeting generation returned no response"
            )

            return Response(
                {
                    "error": "Unable to generate greeting."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "greeting": greeting,
            },
            status=status.HTTP_200_OK,
        )