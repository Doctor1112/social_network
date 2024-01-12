from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, FriendRequest


class UserProfileAdmin(UserAdmin):
    model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FriendRequest)
# Register your models here.
