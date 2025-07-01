from django.urls import path

from core import views

app_name = "core"


urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("sale/", views.sales_view, name="sales"),
]
