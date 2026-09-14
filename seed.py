import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro.settings')
django.setup()

from jet.models import Product

products = [
    {"name": "iPhone 16", "brand": "Apple", "category": "Smartphone", "original_price": 80000.00, "stock": 15, "festival_sale": True},
    {"name": "Samsung Galaxy S25 Ultra", "brand": "Samsung", "category": "Smartphone", "original_price": 95000.00, "stock": 25, "festival_sale": False},
    {"name": "MacBook Air M4", "brand": "Apple", "category": "Laptop", "original_price": 110000.00, "stock": 8, "festival_sale": True},
    {"name": "PlayStation 5", "brand": "Sony", "category": "Gaming Console", "original_price": 55000.00, "stock": 12, "festival_sale": False},
    {"name": "Sony WH-1000XM6", "brand": "Sony", "category": "Headphones", "original_price": 32000.00, "stock": 20, "festival_sale": True},
    {"name": "Apple Watch Series 10", "brand": "Apple", "category": "Smartwatch", "original_price": 50000.00, "stock": 6, "festival_sale": False},
    {"name": "Dell XPS 13", "brand": "Dell", "category": "Laptop", "original_price": 120000.00, "stock": 10, "festival_sale": True},
    {"name": "Canon EOS R50", "brand": "Canon", "category": "Camera", "original_price": 75000.00, "stock": 5, "festival_sale": False},
    {"name": "iPad Air M3", "brand": "Apple", "category": "Tablet", "original_price": 65000.00, "stock": 18, "festival_sale": True},
    {"name": "ASUS ROG Zephyrus G16", "brand": "ASUS", "category": "Laptop", "original_price": 160000.00, "stock": 7, "festival_sale": False},
]

for p in products:
    Product.objects.get_or_create(
        name=p["name"],
        defaults={
            "brand": p["brand"],
            "category": p["category"],
            "original_price": p["original_price"],
            "stock": p["stock"],
            "festival_sale": p["festival_sale"],
        }
    )

print("Successfully seeded products into database!")