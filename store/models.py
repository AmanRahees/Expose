from django.db import models
from products.models import ProductAttribute,Products
from accounts.models import Account

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart_product = models.ForeignKey(Products, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        poff_price = round(self.cart_product.price - self.cart_product.price * self.cart_product.product_name.product_offer /100)
        coff_price = round(self.cart_product.price - self.cart_product.price * self.cart_product.product_name.category_name.category_offer /100)
        if poff_price <= coff_price:
            return poff_price * self.quantity
        else:
            return coff_price * self.quantity

    def __unicode__(self):
        return self.cart_product

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product.product_name