from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import Message


@login_required
def delete_user(request):
    """Delete the currently authenticated user and redirect to home.

    This view deletes request.user which triggers the post_delete signal to
    clean up related messaging data.
    """
    user = request.user
    # Log the user out after deletion might be handled by calling logout, but
    # since the user is deleted we'll simply redirect.
    user.delete()
    return redirect("/")


@login_required
def thread_list(request):
    """List root messages (threads) with one level of replies prefetched."""
    # Use select_related for sender/receiver FKs and prefetch_related for replies
    roots = Message.fetch_thread_root_messages()
    return render(request, "messaging/thread_list.html", {"roots": roots})


@login_required
def thread_detail(request, pk):
    """Display a single thread (root message) with all replies built into a nested tree.

    This uses a single prefetched queryset of all descendant messages and then
    builds an in-memory tree to avoid N+1 queries.
    """
    root = get_object_or_404(Message, pk=pk)

    # Collect all descendants iteratively (BFS) to avoid N+1 queries.
    # We select_related sender/receiver for each query to reduce DB hits.
    all_msgs = [root]
    ids = [root.pk]
    while ids:
        children = list(
            Message.objects.filter(parent_message__in=ids).select_related(
                "sender", "receiver"
            )
        )
        # stop if no more children
        if not children:
            break
        all_msgs.extend(children)
        ids = [m.pk for m in children]

    # Build id->message map and children map in-memory
    msg_map = {m.pk: m for m in all_msgs}
    children = {}
    for m in all_msgs:
        parent_id = getattr(m, "parent_message_id", None)
        children.setdefault(parent_id, []).append(m)

    def build_tree(msg):
        return {
            "message": msg,
            "replies": [build_tree(c) for c in children.get(msg.pk, [])],
        }

    tree = build_tree(root)
    return render(request, "messaging/thread_detail.html", {"tree": tree})


@login_required
def inbox(request):
    """Show messages received by the current user with sender preloaded."""
    # Use the custom manager to fetch unread messages and only retrieve minimal fields.
    qs = (
        Message.unread.unread_for_user(request.user)
        .select_related("sender")
        .only("id", "sender_id", "content", "timestamp")
    )
    return render(request, "messaging/inbox.html", {"messages": qs})


@require_POST
@login_required
def send_message(request):
    """Create a message with sender=request.user and a receiver provided in POST."""
    user_model = get_user_model()
    receiver_id = request.POST.get("receiver_id")
    content = request.POST.get("content", "").strip()
    receiver = get_object_or_404(user_model, pk=receiver_id)

    msg = Message.objects.create(
        sender=request.user, receiver=receiver, content=content
    )
    # Redirect to the thread detail for the created message
    return redirect(reverse("messaging-thread-detail", kwargs={"pk": msg.pk}))
