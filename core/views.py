from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from core.models import User

# Create your views here.


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.get(email=email):
            messages.error(request, "Email has already been used.")
            return redirect("core:register")
        elif User.objects.get(name=name):
            messages.error(
                request, "Name conflict with a name in the database.")
            return redirect("core:register")
        elif password != confirm_password:
            messages.error(request, "Password must match.")
        else:
            user = User.objects.create_user(
                email=email, name=name, password=password)
            login(request, user)
            return redirect("core:sales")
    return render(request, "core/register.html")


def sales_view(request):
    pass
