from django.db import models


class Conversation(models.Model):
    title = models.CharField(
        max_length=120,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Message(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )