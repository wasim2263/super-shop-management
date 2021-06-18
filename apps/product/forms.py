from django import forms

from apps.product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'brand', 'unit_price', 'unit_type', 'stock']
