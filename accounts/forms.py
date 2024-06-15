from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from accounts.models import Accounts
from api.models import Region


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


class UpdateSettingsForm(forms.ModelForm):
    game_name = forms.CharField(required=True)
    tag_line = forms.CharField(required=True)
    region = forms.ChoiceField(required=True, choices=[Region.AMERICAS, Region.ASIA, Region.EUROPE, Region.SEA])

    class Meta:
        model = Accounts
        fields = ["game_name", "tag_line", "region"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["game_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Game Name",
            "type": "text",
            "autocomplete": "off",
            "aria-label": "Game Name",
            "aria-describedby": "gameName",
            "name": "game_name",
            "spnId": "gameName",
            "displayname": "Game Name"
        })

        self.fields["tag_line"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Tag Line",
            "type": "text",
            "autocomplete": "off",
            "aria-label": "Tag Line",
            "aria-describedby": "TagLine",
            "name": "tag_line",
            "spnId": "TagLine"
        })

        self.fields["region"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Region",
            "type": "text",
            "autocomplete": "off",
            "aria-label": "Region",
            "aria-describedby": "Region",
            "name": "region",
            "spnId": "Region"
        })
