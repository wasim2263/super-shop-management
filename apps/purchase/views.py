import json
from io import BytesIO

import qrcode
import qrcode.image.svg

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from num2words import num2words

from apps.customer.models import Customer
from apps.product.models import Product
from apps.purchase.forms import CustomerForm
from apps.purchase.models import Invoice, Purchase


class PurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'customer_form': CustomerForm()
        }
        return render(request, 'purchase/home.html', context)

    def post(self, request):
        purchase_list = request.POST.get('purchase_list', None)
        customer_form = CustomerForm(request.POST)
        customer = None
        if customer_form.is_valid():
            customer = customer_form.save()
        else:
            name = request.POST.get('name', None)
            phone = request.POST.get('phone', None)
            email = request.POST.get('email', None)
            if phone and email and name:
                customers = Customer.objects.filter(Q(phone=phone) | Q(email=email))
                customer = customers.last()
                if customer and customers.count() == 1:
                    customer.name = name
                    customer.phone = phone
                    customer.email = email
                    customer.save()

        if not customer or len(purchase_list) == 0:
            return render(request, 'purchase/home.html', {'customer_form': customer_form})

        invoice = Invoice(customer=customer)
        invoice.save()

        purchase_list = json.loads(purchase_list)
        for item in purchase_list:
            product = None
            if 'id' in item and 'quantity' in item:
                product = Product.objects.filter(id=item['id'], stock__gte=item['quantity']).first()
            if product:
                if product.unit_type == 'piece' and int(item['quantity']) != item['quantity']:
                    continue
                purchase = Purchase(invoice=invoice, product=product,
                                    quantity=item['quantity'], unit_price=product.unit_price)
                purchase.total_price = item['quantity'] * product.unit_price
                purchase.save()
                product.stock -= item['quantity']
                product.save()

        return redirect('purchase:invoice', invoice.id)


class InvoiceView(LoginRequiredMixin, View):
    def get(self, request, invoice_id):
        invoice = Invoice.objects.filter(
            id=invoice_id).prefetch_related('purchase_set', 'purchase_set__product').select_related('customer').first()
        if not invoice:
            raise Http404
        total_amount = invoice.purchase_set.aggregate(Sum('total_price'))['total_price__sum']
        total_amount_in_words = num2words(total_amount)
        factory = qrcode.image.svg.SvgImage
        space_in_words = "\t" * 7
        customer_info = f"Date{space_in_words}: {invoice.created.strftime('%Y-%m-%d')} \nInvoice No\t: {invoice.id} \nName{space_in_words}: " \
                        f"{invoice.customer.name} \n" \
                        f"Phone{space_in_words}: {invoice.customer.phone} \nEmail{space_in_words}: {invoice.customer.email}"
        img = qrcode.make(customer_info, image_factory=factory, box_size=10)
        stream = BytesIO()
        img.save(stream)
        context = {
            'invoice': invoice,
            'total_amount': total_amount,
            'total_amount_in_words': total_amount_in_words.capitalize(),
            'customer_info_qr_code': stream.getvalue().decode()
        }
        return render(request, 'purchase/invoice.html', context=context)
