from django.db import models
from django.urls import reverse
from django.conf import settings
import uuid


class Comment(models.Model):
    
    text = models.TextField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    
    class Meta:
        ordering = ["created"]
    
    def __str__(self):
        return f"{self.author.fullname}: {self.text[:10]}"
    
    
def post_path(instance, filename):
    return f"post_imgs/{instance.author_id}/{instance.pk}_{filename}"

class Post(models.Model):

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)

    text = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=post_path)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.text[:100]
    
    def get_absolute_url(self):
        return reverse("posts:detail", args=[self.pk])
