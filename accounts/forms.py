from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "id": "floatingInput",
            "placeholder": "Username",
            "type": "text"
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "id": "floatingEmail",
            "placeholder": "name@example.com",
            "type": "email"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "id": "floatingPassword",
            "placeholder": "Password",
            "type": "password",
            "autocomplete": "off"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "id": "floatingConfirmPassword",
            "placeholder": "Confirm Password",
            "type": "password",
            "autocomplete": "off"
        })


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "id": "floatingInput",
            "placeholder": "Username",
            "type": "text"
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "id": "floatingPassword",
            "placeholder": "Password",
            "type": "password",
            "autocomplete": "off"
        })
