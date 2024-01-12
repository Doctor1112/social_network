from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.urls import reverse

def avatar_path(instance, filename):
    return f"avatars/{instance.username}/{filename}"

class UserProfile(AbstractUser):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False)
    email = models.EmailField()
    avatar = models.ImageField(
        upload_to=avatar_path, default="default_avatar.jpg"
         )
    friends = models.ManyToManyField("UserProfile", blank=True)
    
    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.fullname
    
    def add_friend(self, user):
        user.friends.add(self)
        self.friends.add(user)
        user.save()
        self.save()
    
    def remove_friend(self, user):
        self.friends.remove(user)
        user.friends.remove(self)
        self.save()
        user.save()
    
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)



class FriendRequest(models.Model):

    sender = models.ForeignKey(UserProfile, 
                               on_delete=models.CASCADE, 
                               related_name="sended_requests")
    receiver = models.ForeignKey(UserProfile, 
                                 on_delete=models.CASCADE,
                                 related_name="received_requests")
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=["sender", "receiver"], name="unique_request")]
    
    def __str__(self) -> str:
        return f"{self.sender.fullname} send {self.receiver.fullname}"
    
