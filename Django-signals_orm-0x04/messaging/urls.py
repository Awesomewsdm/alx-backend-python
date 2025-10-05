from django.urls import path
from . import views

urlpatterns = [
    path("delete-account/", views.delete_user, name="messaging-delete-account"),
    path("threads/", views.thread_list, name="messaging-thread-list"),
    path("threads/<int:pk>/", views.thread_detail, name="messaging-thread-detail"),
    path("inbox/", views.inbox, name="messaging-inbox"),
    path("send/", views.send_message, name="messaging-send-message"),
]
