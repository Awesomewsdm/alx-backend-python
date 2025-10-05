from django.contrib import admin

from .models import Message, Notification
from .models import MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "receiver",
        "timestamp",
        "parent_message",
        "reply_count",
    )
    search_fields = ("sender__username", "receiver__username", "content")

    @admin.display(description="Replies")
    def reply_count(self, obj):
        return obj.replies.count()


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "read", "created_at")
    list_filter = ("read", "created_at")
    search_fields = ("user__username",)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "edited_by", "edited_at")
    search_fields = ("message__content",)
    readonly_fields = ("old_content", "edited_at")
