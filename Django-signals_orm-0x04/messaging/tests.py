from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Message, Notification


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
