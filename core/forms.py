from django.forms import ModelForm

from core.models import Product, Sale


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("balance", "total_amount", "created_by", "updated_by")


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"
        exclude = ("balance", "total_amount", "created_by", "updated_by")
