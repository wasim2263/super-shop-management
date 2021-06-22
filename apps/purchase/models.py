from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

# Create your models here.
from apps.customer.models import Customer
from apps.product.models import Product


class Invoice(SoftDeletableModel, TimeStampedModel):
    customer = models.ForeignKey(Customer,  on_delete=models.RESTRICT)

    def __str__(self):
        return f"invoice:{self.id}-{self.customer}"


class Purchase(SoftDeletableModel, TimeStampedModel):
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, null=True, on_delete=models.RESTRICT)
    quantity = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    unit_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
