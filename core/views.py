from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from core.models import User

# Create your views here.


def index_view(request):
    """
    This view should grab some items from the database to display on the webpage as ads for the company.
    """
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email has already been used.")
            return redirect("core:register")
        elif User.objects.filter(name=name).exists():
            messages.error(
                request, "Name conflict with a name in the database.")
            return redirect("core:register")
        elif password != confirm_password:
            messages.error(request, "Password must match.")
        else:
            user = User.objects.create_user(
                email=email, name=name, password=password)
            user.save()
            login(request, user)
            return redirect("core:sales")
    return render(request, "core/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            User.objects.get(email=email)
        except:
            messages.error(request, "No user with the provided email.")
            return redirect("core:login")
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, "User logged in successfully.")
        return redirect("core:sales")
    return render(request, "core/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("core:index")
    return render(request, "core/logout.html")


def sales_view(request):
    return render(request, "core/sales_list.html")
