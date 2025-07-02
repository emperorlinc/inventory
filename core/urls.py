from django.urls import path

from core import views

app_name = "core"


urlpatterns = [
    path("", views.index_view, name="index"),

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("categories/", views.category_list_view, name="category"),
    path("category/create/", views.category_create_view, name="category-create"),
    path("category/detail/<str:pk>/",
         views.category_detail_view, name="category-detail"),
    path("category/update/<str:pk>/",
         views.category_update_view, name="category-update"),
    path("category/delete/<str:pk>/",
         views.category_delete_view, name="category-delete"),


    path("products/", views.product_list_view, name="products"),
    path("product/create/", views.product_create_view, name="product-create"),

    path("sales/", views.sales_list_view, name="sales"),
    path("sale/create/", views.create_sale_view, name="sale-create"),
]
