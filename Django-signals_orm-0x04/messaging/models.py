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
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    def history(self):
        """Return QuerySet of MessageHistory entries for this message ordered newest first."""
        return MessageHistory.objects.filter(message=self).order_by("-edited_at")


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


class MessageHistory(models.Model):
    """Keeps previous versions of a Message before edits."""

    message = models.ForeignKey(
        Message, related_name="history_entries", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-edited_at"]

    def __str__(self):
        return f"History for message {self.message.pk} at {self.edited_at}"
