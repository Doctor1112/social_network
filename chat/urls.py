from django.contrib import admin
from django.urls import path
from .views import ChatListView, ChatDetailView, OpenChatView

app_name = "chat"

urlpatterns = [
    path("<int:pk>/", ChatDetailView.as_view(), name="chat"),
    path("", ChatListView.as_view(), name="chat_list"),
    path("openchat/<uuid:pk>/", OpenChatView.as_view(), name="open_chat"),
    
]
