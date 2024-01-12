from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Post, Comment
from mixins import OwnerRequiredMixin


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "post_pk"

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.validated_data['post'] = self.get_object()
        serializer.save()

    
class CommentUpdateView(OwnerRequiredMixin, UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pk = request.POST.get("pk")
        action = request.POST.get("action")
        post = get_object_or_404(Post, pk=pk)
        if action == "like":
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        post.save()
        return Response(status=200)