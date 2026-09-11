from django.shortcuts import render
from .models import Product

def product_list(view_request):
    products = Product.objects.all()
    return render(view_request, 'product_list.html', {'products': products})