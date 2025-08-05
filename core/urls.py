from django.urls import path

from core import views

app_name = "core"


urlpatterns = [
    path("", views.index_view, name="index"),

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("user/", views.user_list_view, name="users"),

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
    path("product/detail/<str:pk>/",
         views.product_detail_view, name="product-detail"),
    path("product/update/<str:pk>/",
         views.product_update_view, name="product-update"),
    path("product/delete/<str:pk>/",
         views.product_delete_view, name="product-delete"),

    path("orders/", views.order_list_view, name="orders"),
    path("order/create/", views.order_create_view, name="order-create"),
    path("order/detail/<str:pk>/", views.order_detail_view, name="order-detail"),
    path("order/update/<str:pk>/", views.order_update_view, name="order-update"),
    path("order/delete/<str:pk>/", views.order_delete_view, name="order-delete"),

    path("sales/", views.sale_list_view, name="sales"),
    path("sale/create/", views.sale_create_view, name="sale-create"),
    path("sale/detail/<str:pk>/", views.sale_detail_view, name="sale-detail"),
    path("sale/update/<str:pk>/", views.sale_update_view, name="sale-update"),
    path("sale/delete/<str:pk>/", views.sale_delete_view, name="sale-delete"),
]
