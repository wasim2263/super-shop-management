from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

# Create your models here.
from apps.customer.models import Customer
from apps.product.models import Product


class Invoice(SoftDeletableModel, TimeStampedModel):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)


class Purchase(SoftDeletableModel, TimeStampedModel):
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    unit_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
