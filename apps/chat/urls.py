from django.urls import path

from .views import (
    ChatMessageView,
    ConversationListCreateView,
    DeleteConversationView,
    RegenerateMessageView,
    RenameConversationView,
)


urlpatterns = [
    path(
        "conversations/",
        ConversationListCreateView.as_view(),
    ),
    path(
        "conversations/<int:conversation_id>/rename/",
        RenameConversationView.as_view(),
    ),
    path(
        "conversations/<int:conversation_id>/delete/",
        DeleteConversationView.as_view(),
    ),
    path(
        "chat/",
        ChatMessageView.as_view(),
    ),
    path(
        "regenerate/",
        RegenerateMessageView.as_view(),
    ),
]