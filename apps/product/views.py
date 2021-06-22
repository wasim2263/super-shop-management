from django.contrib import messages
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
        products = Product.objects.filter().order_by('-id')
        search_product = request.GET.get('product_name', "")
        if search_product != "":
            products = products.filter(name__icontains=search_product)
        if request.is_ajax():  # using ajax search in home page
            product_list = products.values('id', 'name', 'stock', 'code', 'unit_price', 'unit_type')[:5]
            return JsonResponse({"product_count": len(product_list), 'products': list(product_list)}, status=200)
        pagination = Paginator(products, 30)
        context = {'products': pagination.get_page(request.GET.get('page'))}

        return render(request, 'product/product-list.html', context=context)


class ProductAddView(LoginRequiredMixin, View):

    def get(self, request, product_id):
        # edit or create view
        if product_id is not None:
            product = get_object_or_404(Product, pk=product_id)
        else:
            product = None
        context = {'form': ProductForm(instance=product), 'product_id': product_id}

        return render(request, 'product/product-add.html', context=context)

    def post(self, request, product_id):
        # update or new create view
        if product_id is not None:  # product_id will be None as it's set in create url
            product = get_object_or_404(Product, pk=product_id)
            message = 'Product updated successfully'
        else:
            product = None
            message = 'Product created successfully'

        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(self.request, message)
            return redirect("product:product-list")
        messages.error(self.request, 'Failed to update product')
        context = {'form': product_form, 'product_id': product_id}
        return render(request, 'product/product-add.html', context=context)


class ProductDetailsView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'product/product-details.html', {"product": product})


class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        if request.user.is_superuser:
            product = Product.objects.filter(id=product_id).first()
            if product:
                product.delete()
                messages.success(self.request, 'Product deleted successfully')
        else:
            messages.warning(self.request, 'Only Admin can delete a product')
        return redirect(request.META.get('HTTP_REFERER'))
