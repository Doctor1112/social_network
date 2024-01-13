from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import FriendRequestSerializer, UserSerializer
from ..models import FriendRequest
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from accounts.utils import accept_friend_request

User = get_user_model()


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_pk = request.POST["user_pk"]
        receiver = get_object_or_404(User, pk=receiver_pk)
        req = FriendRequest.objects.filter(sender=receiver, receiver=request.user).first()
        if req:
            sender = req.sender
            accept_friend_request(req)
            data = UserSerializer(sender).data
            data["status"] = "accepted"
            return Response(data)


        req = FriendRequest.objects.create(sender=request.user, receiver=receiver)
        data = FriendRequestSerializer(req).data
        data["status"] = "sended"
        return Response(data)
    
class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_pk = request.POST["pk"]
        fr_request = get_object_or_404(FriendRequest, pk=request_pk)
        sender = fr_request.sender
        accept_friend_request(fr_request)
        data = UserSerializer(sender).data
        data["status"] = "accepted"
        return Response(data)
    
class RejectFriendRequest(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        fr_request = get_object_or_404(FriendRequest, pk=pk)
        if request.user == fr_request.sender:
            resp_user = fr_request.receiver
        else:
            resp_user = fr_request.sender
        fr_request.delete()
        data = UserSerializer(resp_user).data
        data["status"] = "rejected"
        return Response(data)
    
class RemoveFromFriends(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        friend = get_object_or_404(User, pk=pk)
        user = request.user
        user.remove_friend(friend)
        data = UserSerializer(friend).data
        data["status"] = "removed"
        return Response(data)
    
