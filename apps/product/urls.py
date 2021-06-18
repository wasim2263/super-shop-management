# purchase/urls.py
from django.urls import path

from . import views
app_name = "product"
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('add', views.ProductAddView.as_view(), kwargs={'product_id': None}, name='product-add'),
    path('<int:product_id>/edit', views.ProductAddView.as_view(),  name='product-edit'),
]
