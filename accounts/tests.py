from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.email = "test_user@email.com"
        self.new_username = "test_user_2"
        self.new_email = "test_user_2@email.com"
        self.password = "Password123!$£"
        self.wrong_password = "Wrongpassword123(*$&"
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.home_url = reverse("home")
        self.logout_url = reverse("logout")
        self.settings_url = reverse("settings")

        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

        response = self.client.post(self.register_url, {
            "username": self.new_username,
            "email": self.new_email,
            "password1": self.password,
            "password2": self.password
        })
        self.assertRedirects(response, self.home_url)
        new_user = User.objects.get(username=self.username)
        self.assertTrue(new_user)

    def test_register_view_existing_user(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

        response = self.client.post(self.register_url, {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password
        })
        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertContains(response, "Username or email is already registered")

    def test_login_user_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

        response = self.client.post(self.login_url, {
            "username": self.username,
            "password": self.password
        })
        self.assertRedirects(response, self.home_url)

    def test_login_user_view_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": self.username,
            "password": self.wrong_password
        })
        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertContains(response, "Username or password is incorrect")

    def test_logout_user_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)

    def test_settings_requires_login(self):
        response = self.client.get(self.settings_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.settings_url}")
