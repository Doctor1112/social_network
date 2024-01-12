import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Message
from django.shortcuts import get_object_or_404


class ChatConsumer(WebsocketConsumer):

    
    def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["chat_pk"]
        self.commands = {"new_message": self.new_message,
                        "fetch_prev_msgs": self.fetch_prev_msgs}
        async_to_sync(self.channel_layer.group_add)(
            self.chat_pk, self.channel_name
        )
        self.user = self.scope["user"]
        self.prev_msgs_index = 0
        self.prev_msgs_count = 30
        self.chat = get_object_or_404(Chat, pk=int(self.chat_pk))
        unread = self.chat.messages.filter(read=False).exclude(sender=self.user)
        for msg in unread:
            msg.read = True
            msg.save()
        self.messages = self.chat.messages.all()
        self.accept()

    def new_message(self, msg):
        message = Message.objects.create(sender=self.user, text=msg["message"], chat=self.chat)
        message = self.msg_to_json(message)
        message["command"] = "new_message"
        async_to_sync(self.channel_layer.group_send)(
            self.chat_pk, {"type": "chat.message", "message": message}
        )
    
    def msg_to_json(self, msg):
        return {"text": msg.text,
                           "sender": msg.sender.fullname,
                           "sender_pk": str(msg.sender.pk),
                           "sender_url": msg.sender.get_absolute_url(),
                           "sender_avatar_url": msg.sender.avatar.url,
                           "datetime": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                           "pk": msg.pk
                           }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_pk, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[text_data_json["command"]](text_data_json)
    
    def chat_message(self, event):
        message = event["message"]
        if message.get("sender_pk") != str(self.user.pk):
            msg = get_object_or_404(Message, pk=message.get("pk"))
            msg.read = True
            msg.save()
        self.send(text_data=json.dumps(message))

    def fetch_prev_msgs(self, event):
        messages = self.messages[self.prev_msgs_index: self.prev_msgs_index + self.prev_msgs_count]
        self.prev_msgs_index += self.prev_msgs_count
        messages = list(map(self.msg_to_json, messages))
        self.send(text_data=json.dumps({"command": "prev_messages", "messages": messages}))