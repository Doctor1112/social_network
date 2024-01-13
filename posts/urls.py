from django.contrib import admin
from django.urls import path
from .api.views import CommentCreateView, CommentUpdateView, PostLikeView
from .views import (PostDetailView, PostUpdateView, PostCreateView, 
                    PostDeleteView, FeedView, CommentDeleteView)

app_name = "posts"

urlpatterns = [
    path("<uuid:pk>/", PostDetailView.as_view(), name="detail"),
    path("edit/<uuid:pk>/", PostUpdateView.as_view(), name="edit"),
    path("create/", PostCreateView.as_view(), name="create"),
    path("delete/<uuid:pk>", PostDeleteView.as_view(), name="delete"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("comments/create/<uuid:post_pk>/", CommentCreateView.as_view(), name="comment_create"),
    path("comments/edit/<int:pk>/", CommentUpdateView.as_view(), name="comment_edit"),
    path("comments/delete/<int:pk>/", CommentDeleteView.as_view(), name="comment_delete"),
    path("like/<uuid:pk>/", PostLikeView.as_view(), name="post_like")
]
