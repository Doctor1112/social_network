from rest_framework import serializers
from ..models import Comment
from accounts.api.serializers import UserSerializer
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    created = serializers.SerializerMethodField("created_formatted")
    class Meta:
        model = Comment
        fields = ("text", "author", "created", "pk")
    
    def created_formatted(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M:%S")
