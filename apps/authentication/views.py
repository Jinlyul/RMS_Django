# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from core.settings import GITHUB_AUTH

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None
    print("1. login_view")
    if request.method == "POST":
        print("2. request.method")
        if form.is_valid():
            print("3. form.is_valid() = TRUE")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            print("4. form.is_valid() = FALSE")
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg, "GITHUB_AUTH": GITHUB_AUTH})


def register_user(request):
    msg = None
    success = False
    print("1. register_user")
    if request.method == "POST":
        print("2. request.method")
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("3. form.is_valid() = TRUE")
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            print("4. form.is_valid() = FALSE")
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
