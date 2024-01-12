import datetime
from django import template
from accounts.models import FriendRequest

register = template.Library()

@register.simple_tag
def get_data_for_fr_button(cur_user, user):
    recv_req = cur_user.received_requests.all()
    for req in recv_req:
        if req.sender_id == user.pk:
            return {"pk": req.pk, "id": "reject_request", "text": "Отклонить заявку"}
    send_req = cur_user.sended_requests.all()
 
    for req in send_req:
        if req.receiver_id == user.pk:
            return {"pk": req.pk, "id": "cancel_request", "text": "Отменить заявку"}
    if user in cur_user.friends.all():
        return {"pk": user.pk, "id": "remove_friend", "text": "Удалить из друзей"}
    
    return {"pk": user.pk, "id": "add_friend", "text": "Добавить в друзья"}
    