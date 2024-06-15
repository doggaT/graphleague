import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm, UpdateSettingsForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Accounts


logger = logging.getLogger(__name__)


@login_required(login_url="login")
def home(request):
    return render(request, "accounts/me.html")


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return redirect("home")
        else:
            messages.info(request, "Username or email is already registered")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login_user(request):
    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("home")
        else:
            messages.info(request, "Username or password is incorrect")

    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout_user(request):
    auth.logout(request)
    return redirect("home")


def settings(request):
    accounts = Accounts()
    form = UpdateSettingsForm()

    if request.user.is_authenticated:
        user_account = accounts.get_game_name_tag_line_by_user_id(request.user.id)
        form = UpdateSettingsForm(request.POST, instance=user_account)

        if request.method == "POST":
            form = UpdateSettingsForm(request.POST, instance=user_account)
            if form.is_valid():
                form.save()
                game_name = form.cleaned_data["game_name"]
                tag_line = form.cleaned_data["tag_line"]
                region = form.cleaned_data["region"]
                logger.info(f"Updated game name {game_name} and tag line {tag_line}")
                accounts.add_or_update_game_name_tag_line(request.user.id, region, game_name, tag_line)

    context = {"form": form}

    return render(request, "accounts/settings.html", context)
