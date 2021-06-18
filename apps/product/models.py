from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

# Create your models here.
PRODUCT_UNIT_TYPES = (
    ('kg', 'KG'),
    ('piece', 'Piece'),
    ('litre', 'Litre')
)


class Category(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Brand(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(SoftDeletableModel, TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    unit_type = models.CharField(max_length=20, choices=PRODUCT_UNIT_TYPES)
    stock = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
