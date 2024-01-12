from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FriendRequest
from posts.forms import PostForm
from chat.models import Message
from django.core.paginator import Paginator
from mixins import PaginateMixin, UserPrefetchRelatedrMixin

User = get_user_model()

class ProfileDetailView(LoginRequiredMixin, PaginateMixin, DetailView):
    model = User
    template_name = "account/profile.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        is_current_user = self.request.user == self.object
        friends = self.object.friends.all()
        context["is_current_user"] = is_current_user
        context["friends_cnt"] = friends.count()
        context["form"] = PostForm()
        return context
    
    def get_paginate_queryset(self):
        return self.object.posts.select_related("author").prefetch_related("likes", "comments")
    




class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    fields = ("first_name", "last_name", "avatar")
    template_name = "account/profile_edit.html"
    model = User

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user
    

class FriendsListView(UserPrefetchRelatedrMixin, PaginateMixin, LoginRequiredMixin, DetailView):
    template_name = "account/friends_list.html"
    model = User
    pk_url_kwarg = "user_pk"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["visited_user"] = self.object
        return context
    
    
    def get_paginate_queryset(self):
        return self.object.friends.all()
    
    
class FriendReceivedRequestList(LoginRequiredMixin, ListView):

    template_name = "account/friend_received_request_list.html"
    paginate_by = 10
    

    def get_queryset(self) -> QuerySet[Any]:
        qs = FriendRequest.objects.filter(receiver=self.request.user).select_related("sender")
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["visited_user"] = self.request.user
        return context

    
class FriendSendedRequestList(LoginRequiredMixin, ListView):

    template_name = "account/friend_sended_request_list.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = FriendRequest.objects.filter(sender=self.request.user).select_related("receiver")
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["visited_user"] = self.request.user
        return context





class FindFriendsView(UserPrefetchRelatedrMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = "account/users_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().exclude(pk=self.request.user.pk)
        q = self.request.GET["q"]
        if len(q) > 0:
            first_name, last_name = q.split()
            qs = qs.filter(first_name__iexact=first_name,
                                        last_name__iexact=last_name)
        return qs



