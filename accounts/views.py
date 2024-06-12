from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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


def settings():
    pass
