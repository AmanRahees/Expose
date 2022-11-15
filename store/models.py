from django.db import models
from products.models import Products, Variation
from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart =models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.cart_product.price * self.quantity

    def __unicode__(self):
        return self.cart_product