from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Chat, Message
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, F, Q, Subquery, OuterRef, Prefetch

User = get_user_model()


class ChatListView(LoginRequiredMixin,  ListView):

    template_name = "chat/chat_list.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        sq = Subquery(
            Message.objects.filter(
                chat_id=OuterRef('chat_id')
                ).values_list('id', flat=True)[:1]
            )

        qs = self.request.user.chats.prefetch_related("members").prefetch_related(
            Prefetch("messages",
                     queryset=Message.objects.filter(id__in=sq))).annotate(
                        unread_count=Count(
                            'messages', filter=(Q(messages__read=False) & ~Q(messages__sender=self.request.user))), msg_timestamp=Max("messages__timestamp")
                            ).order_by("-msg_timestamp").exclude(messages__isnull=True)
        

        return qs




class ChatDetailView(LoginRequiredMixin, DetailView):

    model = Chat
    template_name = "chat/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        context["chat_name"] = self.object.chat_name(self.request.user)
        context["chat_img"] = self.object.chat_img(self.request.user)
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().prefetch_related("members")


class OpenChatView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        chat = Chat.objects.filter(members=user).filter(members=request.user)
        if not chat:
            chat = Chat.objects.create()
            chat.members.add(user, request.user)
            chat.save()
        else:
            chat = chat[0]
        return redirect("chat:chat", pk=chat.pk)
