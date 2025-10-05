import unittest

try:
    from django.test import TestCase  # type: ignore
except Exception:
    TestCase = unittest.TestCase

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
        self.assertIsNotNone(notif)

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

    def test_deleting_user_cleans_related_data(self):
        # Create a message and history, then delete the user and assert cleanup
        msg = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="To be deleted"
        )
        # simulate edit
        msg.content = "Edited"
        msg.save()

        # create a notification for bob (post_save should have created it)
        # now delete bob
        self.bob.delete()

        # Messages where bob was receiver should be deleted
        self.assertFalse(Message.objects.filter(pk=msg.pk).exists())

        # Notifications for bob should be deleted
        self.assertFalse(Notification.objects.filter(user=self.bob).exists())

        # MessageHistory entries where edited_by is None may still exist, but
        # entries explicitly referencing the deleted user should be gone
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.bob).exists())

    def test_threaded_conversation_retrieval(self):
        # Create a root message and replies
        root = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Root"
        )
        r1 = Message.objects.create(
            sender=self.bob, receiver=self.alice, content="Reply 1", parent_message=root
        )
        r2 = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Reply 2", parent_message=root
        )
        r1_1 = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Reply 1.1", parent_message=r1
        )

        # Use the helper to fetch root messages with prefetching
        qs = Message.fetch_thread_root_messages()
        self.assertIn(root, list(qs))

        # Ensure get_thread returns a nested structure
        t = root.get_thread()
        self.assertEqual(t["message"], root)
        self.assertEqual(len(t["replies"]), 2)
        # check nested reply
        first_reply = [r for r in t["replies"] if r["message"].pk == r1.pk][0]
        self.assertEqual(len(first_reply["replies"]), 1)

    def test_unread_manager_filters_unread(self):
        # create two messages, mark one as read
        m1 = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Unread"
        )
        m2 = Message.objects.create(
            sender=self.alice, receiver=self.bob, content="Read"
        )
        m2.read = True
        m2.save()

        unread_qs = Message.unread.unread_for_user(self.bob)
        self.assertIn(m1, list(unread_qs))
        self.assertNotIn(m2, list(unread_qs))
