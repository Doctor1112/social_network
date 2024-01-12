from chat.models import Message

def unread_msgs_cnt(request):
    if request.user.is_authenticated:
        unread_msgs_cnt = Message.unread.exclude(sender=request.user).filter(chat__in=request.user.chats.all()).count()
        return {"unread_msgs_cnt": unread_msgs_cnt}
    return {}

def received_friend_requests_cnt(request):
    if request.user.is_authenticated:
        cnt = request.user.received_requests.count()
        return {"received_frnd_req_cnt": cnt}
    return {}
