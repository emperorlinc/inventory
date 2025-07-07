from django.forms import ModelForm

from core.models import Category, Order, Product, Sale


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("created_by", "updated_by")


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ("balance", "total_amount", "created_by", "updated_by")


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"
        exclude = ("balance", "total_amount", "created_by", "updated_by")
