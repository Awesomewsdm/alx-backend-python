from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Message, Notification
from .models import MessageHistory


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
