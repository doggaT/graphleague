from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class PlayerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.email = "test_user@email.com"
        self.password = "Password123!$£"
        self.login_url = reverse("login")
        self.my_stats_url = reverse("my-stats")

        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_my_stats_requires_login(self):
        response = self.client.get(self.my_stats_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.my_stats_url}")
