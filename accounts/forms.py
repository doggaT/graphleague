from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["id"] = "floatingInput"
        self.fields["username"].widget.attrs["placeholder"] = "username"
        self.fields["username"].widget.attrs["type"] = "username"

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["id"] = "floatingEmail"
        self.fields["email"].widget.attrs["placeholder"] = "name@example.com"

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["id"] = "floatingPassword"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["id"] = "floatingConfirmPassword"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["id"] = "floatingInput"
        self.fields["username"].widget.attrs["placeholder"] = "username"
        self.fields["username"].widget.attrs["type"] = "username"

        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["id"] = "floatingPassword"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
