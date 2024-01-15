from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

User = get_user_model()


class PostsTests(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create_user(username="user", password="123")
        self.user_2 = User.objects.create_user(username="user_2", password="123")
        self.user_1.add_friend(self.user_2)
        self.post_1 = Post.objects.create(text="text_post_1", author=self.user_1)
        self.post_2 = Post.objects.create(text="text_post_2", author=self.user_2)

    def test_feed_contains_post(self):
        self.client.force_login(self.user_1)
        resp = self.client.get(reverse("posts:feed"))
        self.assertContains(resp, "text_post_2")

    def test_profile_contains_post(self):
        self.client.force_login(self.user_2)
        resp = self.client.get(self.user_1.get_absolute_url())
        self.assertContains(resp, "text_post_1")

    def test_post_edit_forbidden(self):
        self.client.force_login(self.user_2)
        res = self.client.post(
            reverse("posts:edit", kwargs={"pk": self.post_1.pk}),
            data={"text": "sometext"}
            )
        self.assertEqual(res.status_code, 403)

    def test_post_delete_forbidden(self):
        self.client.force_login(self.user_2)
        res = self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post_1.pk}),
            data={"text": "sometext"}
            )
        self.assertEqual(res.status_code, 403)


