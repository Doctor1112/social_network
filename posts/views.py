from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.http import JsonResponse
from mixins import OwnerRequiredMixin, PaginateMixin
# Create your views here.


class PostDetailView(PaginateMixin, DetailView):
    model = Post
    template_name = "posts/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
    
    def get_paginate_queryset(self):
        return self.object.comments.select_related("author").all()
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().prefetch_related("likes", "comments")


class PostUpdateView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/update.html"

    def get_success_url(self) -> str:
        return self.request.user.get_absolute_url()


class PostDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    
    def get_success_url(self) -> str:

        return self.request.user.get_absolute_url()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ("text", "image")
    template_name = "posts/create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return self.request.user.get_absolute_url()
    

class FeedView(LoginRequiredMixin, ListView):

    template_name = "posts/feed.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        friends = self.request.user.friends.all()
        friends_posts = Post.objects.filter(author__in=friends).select_related("author").prefetch_related("likes").prefetch_related("comments")
        return friends_posts
    

class CommentDeleteView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "posts/comment_confirm_delete.html"
    

    def get_success_url(self) -> str:
        return self.object.post.get_absolute_url()
    
class CommentUpdateView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):

    model = Comment
    template_name = "posts/comment_update.html"

    def get_success_url(self) -> str:
        return self.object.post.get_absolute_url()
    

    
