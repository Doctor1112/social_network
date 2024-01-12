from rest_framework import serializers
from ..models import UserProfile, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = UserProfile
        fields = ("url", "fullname", "id", "avatar")

class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = "__all__"