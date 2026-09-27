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


class Memory(models.Model):
    MEMORY_TYPE_CHOICES = [
        ("PREFERENCE", "Preference"),
        ("USER_FACT", "User Fact"),
        ("PROJECT_CONTEXT", "Project Context"),
        ("INSTRUCTION", "Instruction"),
    ]

    type = models.CharField(
        max_length=30,
        choices=MEMORY_TYPE_CHOICES,
    )
    content = models.TextField()
    confidence = models.FloatField(
        default=1.0,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-updated_at",
        ]