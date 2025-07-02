from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from core.forms import CategoryForm, ProductForm, SaleForm
from core.models import Category, Product, User, Sale

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


def category_list_view(request):
    page = "Category"

    categories = Category.objects.all()
    return render(request, "core/category/category_list.html", {"categories": categories, "page": page})


def category_detail_view(request, pk):
    page = "Category Product"

    try:
        category = Category.objects.get(id=pk)
        products = Product.objects.filter(category=category)
    except:
        messages.error(request, "No category with the provided id.")
        return redirect("core:category")

    return render(request, "core/category/category_detail.html", {"products": products, "category": category, "page": page})


def category_create_view(request):
    page = "Category Create"

    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("core:category")
        else:
            messages.error(request, "Provide a valid category name.")
            return redirect("core:category-create")
    return render(request, "core/category/category_create.html", {"form": form, "page": page})


def category_update_view(request, pk):
    page = "Category Update"

    try:
        category = Category.object.get(id=pk)
    except:
        messages.error(request, "No category with the provided id.")
        return redirect(reverse("core:category-update",  kwargs={"id": pk}))

    form = CategoryForm(instance=category)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("core:category")
        else:
            messages.error(request, "Invalid value provided.")
            return redirect(reverse("core:category-update", kwargs={"id": pk}))
    return render(request, "core/category/category_update.html", {"form": form, "page": page})


def category_delete_view(request, pk):
    page = "Category Delete"

    try:
        category = Category.objects.get(id=pk)
    except:
        messages.error(request, "No category with the provided id.")
        return redirect("core:category")

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("core:category")
    return render(request, "core/delete.html", {"obj": category, "page": page})


def product_list_view(request):
    page = "Products"

    products = Product.objects.all()
    return render(request, "core/product/product_list.html", {"products": products, "page": page})


def product_detail_view(request, pk):
    page = "Product Detail"
    try:
        product = Product.objects.get(id=pk)
    except:
        messages.error(request, "No product with the provided id.")
        return redirect("core:products")
    return render(request, "core/product/product_detail.html", {"product": product, "page": page})


def product_create_view(request):
    page = "Product Create"

    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
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


def product_update_view(request, pk):
    page = "Product Update"

    try:
        product = Product.objects.get(id=pk)
    except:
        messages.error(request, "No product with the provided id.")
        return redirect(reverse("core:product-detail", kwargs={"id": pk}))

    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect(reverse("core:product-detail", kwargs={"id": pk}))
        else:
            messages.error(request, "Invalid values provided.")
            return redirect(reverse("core:product-update", kwargs={"id": pk}))
    return render(request, "core/product/product_update.html", {"form": form, "page": page})


def product_delete_view(request, pk):
    page = "Product Delete"

    try:
        product = Product.objects.get(id=pk)
    except:
        messages.error(request, "No product with the provided id.")
        return redirect("core:products")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("core:products")
    return render(request, "core/delete.html", {"obj": product, "page": page})


def sales_list_view(request):
    page = "Sales"

    sales = Sale.objects.all()
    return render(request, "core/sale/sales_list.html", {"sales": sales, "page": page})


def sale_detail_view(request, pk):
    page = "Sale Detail"

    try:
        sale = Sale.objects.get(id=pk)
    except:
        messages.error(request, "No sale with the provided id.")
        return redirect("core:sales")

    return render(request, "core/sale/sale_detail.html", {"sale": sale, "page": page})


def sale_create_view(request):
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


def sale_update_view(request, pk):
    page = "Sale Update"

    try:
        sale = Sale.objects.get(id=pk)
    except:
        messages.error(request, "No sale with the provided id.")
        return redirect(reverse("core:sale-detail", kwargs={"id": pk}))

    form = SaleForm(instance=sale)
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)

        if form.is_valid():
            form.save(commit=False)
            form.updated_by = request.user
            form.save()
            messages.success(request, "Sale updated successfully.")
            return redirect(reverse("core:sale-detail", kwargs={"id": pk}))
        else:
            messages.error(request, "Invalid values provided.")
            return redirect(reverse("core:sale-update", kwargs={"id": pk}))
    return render(request, "core/sale/sale_update.html", {"form": form, "page": page})


def sale_delete_view(request, pk):
    page = "Sale Delete"

    try:
        sale = Sale.objects.get(id=pk)
    except:
        messages.error(request, "No sale for the provided id.")
        return redirect("core:sales")
    if request.method == "POST":
        sale.delete()
        messages.success(request, "Sale deleted successfully.")
        return redirect("core:sales")
    return render(request, "core/delete.html", {"obj": sale, "page": page})
