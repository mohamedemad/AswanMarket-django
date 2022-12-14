from django.db import models

# Create your models here.
from store.models import Product


class Carts(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    carts = models.ForeignKey(Carts, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product
