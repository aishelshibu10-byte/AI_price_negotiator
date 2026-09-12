

# Register your models here.
from django.contrib import admin
from .models import Product, CustomerProfile

admin.site.register(Product)
admin.site.register(CustomerProfile)