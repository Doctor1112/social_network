from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import FriendRequest

User = get_user_model()


class FriendReqTests(TestCase):
    def setUp(self) -> None:
        self.sender = User.objects.create_user(username="user", password="123")
        self.receiver = User.objects.create_user(username="user_2", password="123")
        self.fr_request = FriendRequest.objects.create(
            sender=self.sender, receiver=self.receiver
        )

    def test_friend_req_btn_sender_profile(self):
        self.client.force_login(self.sender)
        resp = self.client.get(self.receiver.get_absolute_url())
        self.assertContains(resp, "Отменить заявку")
        self.assertContains(resp, "cancel_request")

    def test_friend_req_btn_receiver_profile(self):
        self.client.force_login(self.receiver)
        resp = self.client.get(self.sender.get_absolute_url())
        self.assertContains(resp, "Отклонить заявку")
        self.assertContains(resp, "reject_request")
        self.assertContains(resp, "Принять заявку")
        self.assertContains(resp, "accept_request")

    def test_accept_request(self):
        self.client.force_login(self.receiver)
        resp = self.client.post(
            reverse("accounts:accept_friend_request",
                    kwargs={"pk": self.fr_request.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.sender in self.receiver.friends.all())

    def test_reject_request(self):
        self.client.force_login(self.sender)
        resp = self.client.delete(
            reverse("accounts:reject_friend_request",
                    kwargs={"pk": self.fr_request.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_cancel_request(self):
        self.client.force_login(self.receiver)
        resp = self.client.delete(
            reverse("accounts:reject_friend_request",
                    kwargs={"pk": self.fr_request.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_send_request_forbidden(self):
        resp = self.client.post(
            reverse("accounts:send_friend_request",
                    kwargs={"receiver_pk": self.receiver.pk})
        )
        self.assertEqual(resp.status_code, 403)
    
    def test_reject_not_existing_request(self):
        self.client.force_login(self.receiver)
        resp = self.client.delete(
            reverse("accounts:reject_friend_request", kwargs={"pk": 100})
            )
        self.assertEqual(resp.data["status"], "request not found")
        

