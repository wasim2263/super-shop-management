# purchase/urls.py
from django.urls import path

from . import views
app_name = "purchase"

urlpatterns = [
    path('', views.PurchaseView.as_view(), name='home'),
    path('invoice/<int:invoice_id>', views.InvoiceView.as_view(), name='invoice'),
]
