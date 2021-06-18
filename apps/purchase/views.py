from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.product.models import Product


class PurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'purchase/home.html', context)
