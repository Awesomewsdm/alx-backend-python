from django.conf import settings
from django.db import models


class Message(models.Model):
    """Simple message sent from one user to another."""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class Notification(models.Model):
    """Notification created when a user receives a Message."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message, related_name="notifications", on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user} - message {self.message.pk}"
