# purchase/urls.py
from django.urls import path

from . import views
app_name = "product"
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('add', views.ProductAddView.as_view(), kwargs={'product_id': None}, name='product-add'),
    path('<int:product_id>/edit', views.ProductAddView.as_view(),  name='product-edit'),
    path('<int:product_id>/details', views.ProductDetailsView.as_view(),  name='product-details'),
    path('<int:product_id>/delete', views.ProductDeleteView.as_view(),  name='product-delete'),
]
