from django.forms import ModelForm

from core.models import Category, Product, Sale


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("balance", "total_amount", "created_by",
                   "updated_by", "total_quantity")


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"
        exclude = ("balance", "total_amount", "created_by", "updated_by")
