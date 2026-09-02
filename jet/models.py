
# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    original_price = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)
    stock = models.IntegerField(default=10)
    festival_sale = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"