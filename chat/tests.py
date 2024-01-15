from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Message, Chat
from channels.testing import WebsocketCommunicator
from .consumers import ChatConsumer

User = get_user_model()


class ChatTests(TestCase):
    def setUp(self) -> None:
        self.sender = User.objects.create_user(username="user", password="123", first_name="fname_1", last_name="lname_1")
        self.receiver = User.objects.create_user(username="user_2", password="123", first_name="fname_2", last_name="lname_2")
        self.chat = Chat.objects.create()
        self.chat.members.add(self.sender, self.receiver)
        self.msg = Message.objects.create(chat=self.chat, text='text', sender=self.sender)


    def test_chat_name(self):
        self.assertEqual(self.chat.chat_name(self.sender), self.receiver.fullname)
        self.assertEqual(self.chat.chat_name(self.receiver), self.sender.fullname)

    def test_chat_list_contains_chat(self):
        self.client.force_login(self.receiver)
        resp = self.client.get(reverse("chat:chat_list"))
        self.assertContains(resp, self.msg.text)
        self.assertContains(resp, self.sender.fullname)

