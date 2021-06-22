from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from apps.purchase.models import Purchase, Invoice


class PurchaseAdmin(admin.TabularInline):
    model = Purchase
    classes = ['collapse', ]


@admin.register(Invoice)
class BusinessAdmin(ModelAdmin):
    inlines = [PurchaseAdmin]
