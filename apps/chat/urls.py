from django.urls import path

from .views import (
    ChatMessageView,
    ConversationListCreateView,
    RegenerateMessageView,
)


urlpatterns = [
    path("conversations/", ConversationListCreateView.as_view()),
    path("chat/", ChatMessageView.as_view()),
    path("regenerate/", RegenerateMessageView.as_view()),
]