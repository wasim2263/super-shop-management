from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View

from apps.product.forms import ProductForm
from apps.product.models import Product


class ProductListView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        products = Product.objects.filter()
        search_product = request.GET.get('product_name', "")
        if search_product != "":
            products = products.filter(name__icontains=search_product)
        if request.is_ajax():
            product_list = products.values('id', 'name', 'stock', 'code', 'unit_price', 'unit_type')[:10]
            return JsonResponse({"product_count": len(product_list), 'products': list(product_list)}, status=200)
        pagination = Paginator(products, 30)
        context['products'] = pagination.get_page(request.GET.get('page'))
        return render(request, 'product/product-list.html', context)


class ProductAddView(LoginRequiredMixin, View):

    def get(self, request, product_id):
        if product_id is not None:
            product = get_object_or_404(Product, pk=product_id)
        else:
            product = None
        context = {'form': ProductForm(instance=product), 'product_id': product_id}

        return render(request, 'product/product-add.html', context=context)

    def post(self, request, product_id):
        if product_id is not None:
            product = get_object_or_404(Product, pk=product_id)
        else:
            product = None
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect("product:product-list")
        context = {'form': product_form, 'product_id': product_id}
        return render(request, 'product/product-add.html', context=context)
