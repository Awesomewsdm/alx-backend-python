from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from messaging.models import Message


@cache_page(60)  # cache this view for 60 seconds
def conversation_messages(request, message_pk):
    """Display messages in a conversation (thread) — cached for 60s."""
    root = get_object_or_404(Message, pk=message_pk)

    # Efficiently fetch root and immediate replies (select_related/prefetch_related)
    root = (
        Message.objects.filter(pk=root.pk)
        .select_related("sender", "receiver")
        .prefetch_related("replies", "replies__sender")
    ).first()

    # Build a simple context — templates should render replies recursively
    return render(request, "chats/conversation.html", {"root": root})
