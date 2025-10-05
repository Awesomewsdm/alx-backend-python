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
    parent_message = models.ForeignKey(
        "self", related_name="replies", null=True, blank=True, on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    def history(self):
        """Return QuerySet of MessageHistory entries for this message ordered newest first."""
        return MessageHistory.objects.filter(message=self).order_by("-edited_at")

    def get_thread(self):
        """Return this message and all replies recursively as a nested dict.

        Note: This method uses the `replies` related_name and will be efficient
        if the caller prefetched `replies` and `replies__sender` via
        `prefetch_related('replies', 'replies__replies')` or similar.
        """

        def _gather(msg):
            return {"message": msg, "replies": [_gather(r) for r in msg.replies.all()]}

        return _gather(self)

    @staticmethod
    def fetch_thread_root_messages(qs=None):
        """Return queryset of root messages (no parent) with replies prefetched.

        Use select_related for FK to user and prefetch_related for replies to
        minimize query count when rendering threads.
        """
        qs = qs if qs is not None else Message.objects.all()
        return (
            qs.filter(parent_message__isnull=True)
            .select_related("sender", "receiver")
            .prefetch_related("replies", "replies__sender", "replies__replies")
        )


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
