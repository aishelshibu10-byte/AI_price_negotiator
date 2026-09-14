from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10)
    festival_sale = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"


class CustomerProfile(models.Model):
    SEGMENT_CHOICES = [
        ('NEW', 'New'),
        ('RETURNING', 'Returning'),
        ('PREMIUM', 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    segment = models.CharField(max_length=20, choices=SEGMENT_CHOICES, default='NEW')
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_segment(self):
        if self.total_orders == 0:
            self.segment = 'NEW'
        elif self.total_spent >= 50000 or self.total_orders >= 5:
            self.segment = 'PREMIUM'
        else:
            self.segment = 'RETURNING'
        self.save()

    def __str__(self):
        return f"{self.user.username} ({self.segment})"


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiated = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    @property
    def subtotal(self):
        return self.agreed_price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity} (₹{self.agreed_price})"