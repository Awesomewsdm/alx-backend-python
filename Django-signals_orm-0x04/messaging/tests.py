try:
    from django.test import TestCase  # type: ignore
except Exception:
    from unittest import TestCase

from django.contrib.auth import get_user_model  # type: ignore


from .models import Message, Notification
from .models import MessageHistory


User = get_user_model()


class MessagingSignalTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="password")
        self.bob = User.objects.create_user(username="bob", password="password")

    def test_message_creates_notification_for_receiver(self):
        # When Alice sends a message to Bob, a Notification should be created for Bob
        msg = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Hello Bob"
        )

        notifications = Notification.objects.filter(user=self.bob, message=msg)
        self.assertEqual(notifications.count(), 1)
        notif = notifications.first()
        self.assertFalse(notif.read)

    def test_editing_message_creates_history(self):
        msg = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Original"
        )

        # Edit the message
        msg.content = "Edited"
        msg.save()

        histories = MessageHistory.objects.filter(message=msg)
        self.assertEqual(histories.count(), 1)
        hist = histories.first()
        self.assertEqual(hist.old_content, "Original")
        # message should be marked as edited
        msg.refresh_from_db()
        self.assertTrue(msg.edited)
