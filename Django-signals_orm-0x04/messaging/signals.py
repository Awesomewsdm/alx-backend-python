from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete

from .models import Message, Notification
from .models import MessageHistory
from django.contrib.auth import get_user_model


@receiver(post_delete, sender=get_user_model())
def cleanup_user_related_data(sender, instance, **kwargs):
    """Ensure messages, notifications and message histories related to a user are removed.

    Note: Many of these will be removed by FK `on_delete=CASCADE` but we explicitly
    delete related objects that reference the user directly (notifications, history
    entries where edited_by references the user) to ensure no orphaned data remains.
    """
    # Delete notifications that belong to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message history entries where this user was recorded as the editor
    MessageHistory.objects.filter(edited_by=instance).delete()

    # Delete messages where the user was sender or receiver (cascades to related objects)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """Create a Notification for the receiver whenever a new Message is created."""
    if not created:
        return

    Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Before a Message is updated, save the old content into MessageHistory.

    Note: pre_save runs for creates as well; we only act when the instance already
    exists in the database (i.e., has a PK and is not being created).
    """
    if instance.pk is None:
        # New message, nothing to log
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content changed, record the old content
    if old.content != instance.content:
        MessageHistory.objects.create(message=instance, old_content=old.content)
        # mark the message as edited
        instance.edited = True
