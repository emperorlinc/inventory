from django.urls import path

from core import views

app_name = "core"


urlpatterns = [
    path("", views.index_view, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("sale/", views.sales_view, name="sales"),
]
