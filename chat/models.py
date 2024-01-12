from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.urls import reverse
import uuid
from django.db.models import Subquery, OuterRef


class UnReadManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(read=False)


class Chat(models.Model):

    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name="chats")
    name = models.CharField(max_length=100, blank=True, null=True)

    def chat_name(self, user):
        if self.name:
            return self.name
        for member in self.members.all():
            if user != member:
                return member.fullname
            
    def get_absolute_url(self):
        return reverse("chat:chat", kwargs={"pk": self.pk})
    
    def last_message(self):
        return self.messages.all()[0]
    
    def chat_img(self, user):
        for member in self.members.all():
            if user != member:
                return member.avatar.url
    
    def __str__(self):
        name = ""
        for user in self.members.all():
            name += f"{user.username}_"
        return name.strip("_")


class Message(models.Model):

    text = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,
                             related_name="messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    objects = models.Manager()
    unread = UnReadManager()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sender.username} {self.timestamp} {self.text[:15]}"

