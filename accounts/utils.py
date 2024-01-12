def accept_friend_request(req):
    sender = req.sender
    receiver = req.receiver
    receiver.add_friend(sender)
    req.delete()