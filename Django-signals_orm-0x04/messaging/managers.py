from django.db import models


class UnreadMessagesManager(models.Manager):
    """Manager to filter unread messages for a given user."""

    def unread_for_user(self, user):
        # Messages received by the user and not read yet
        return self.get_queryset().filter(receiver=user, read=False)
