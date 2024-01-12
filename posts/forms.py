from django.forms import ModelForm, Textarea
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "image"]
        widgets = {
            'text': Textarea(attrs={'cols': 20, 'rows': 5, }),
        }
        labels = {"text": "Текст",
                  "image": "Изображение"}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text", )
        labels = {"text": "Текст",
                  }
        