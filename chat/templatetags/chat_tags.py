import datetime
from django import template
from accounts.models import FriendRequest

register = template.Library()

@register.simple_tag
def get_chat_name(chat, user):
    return chat.chat_name(user)

@register.simple_tag
def get_chat_img(chat, user):
    return chat.chat_img(user)


    