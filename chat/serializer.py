from rest_framework import serializers
from .models import Message
from accounts.api.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    created = serializers.SerializerMethodField("created_formatted")

    class Meta:
        model = Message
        fields = "__all__"

    def created_formatted(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M:%S")
    