from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from core.forms import ProductForm, SaleForm
from core.models import Product, User, Sale

# Create your views here.


def index_view(request):
    page = "Show Room"

    """
    This view should grab some items from the database to display on the webpage as ads for the company.
    """
    return render(request, "index.html", {"page": page})


def register_view(request):
    page = "Register"

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
    return render(request, "core/authentication/register.html", {"page": page})


def login_view(request):
    page = "Login"

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
    return render(request, "core/authentication/login.html", {"page": page})


def logout_view(request):
    page = "Logout"

    if request.method == "POST":
        logout(request)
        return redirect("core:index")
    return render(request, "core/authentication/logout.html", {"page": page})


def product_list_view(request):
    page = "Products"

    products = Product.objects.all()
    return render(request, "core/product/product_list.html", {"products": products, "page": page})


def product_create_view(request):
    page = "Product Create"

    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.total_quantity = form.total_quantity_func
            form.total_amount = form.total_func
            form.balance = form.balance_func
            form.created_by = request.user
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect("core:products")
        else:
            messages.error(request, "Invalid form.")
            return redirect("core:product-create")

    return render(request, "core/product/product_create.html", {"form": form, "page": page})


def sales_list_view(request):
    page = "Sales"

    sales = Sale.objects.all()
    return render(request, "core/sale/sales_list.html", {"sales": sales, "page": page})


def create_sale_view(request):
    page = "Sale Create"

    form = SaleForm()

    if request.method == "POST":
        form = SaleForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.total_amount = form.total_func
            form.balance = form.balance_func
            form.created_by = request.user

            # Todo: Rectify the total quantity property func in the signals

            form.save()
            messages.success(request, "Sale created successfully.")
            return redirect("core:sales")
        else:
            messages.error(request, "Invalid form.")
            return redirect("core:sale-create")
    return render(request, "core/sale/sale_create.html", {"form": form, "page": page})
