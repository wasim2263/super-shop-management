# purchase/urls.py
from django.urls import path

from . import views
app_name = "purchase"

urlpatterns = [
    path('', views.PurchaseView.as_view(), name='home'),
]
