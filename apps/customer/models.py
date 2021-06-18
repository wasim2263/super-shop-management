from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

# Create your models here.
from apps.product.models import Product


class Customer(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=13, unique=True)
    email = models.CharField(max_length=255, unique=True, null=True)
