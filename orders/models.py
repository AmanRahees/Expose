from django.db import models
from accounts.models import *
from products.models import Products

# Create your models here.

class useraddress(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField("you name",max_length=256)
    mobile = models.CharField(max_length=32, default="1")
    email = models.CharField(max_length=140, default='1')
    address = models.CharField(max_length=1024)
    address_2 = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=256)
    district = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    pincode = models.CharField(max_length=6)
    created_at = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "User Address"

    def __str__(self):
        return self.user_id.first_name + "'s address"

class Order(models.Model):
    user =  models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=30, null=False)
    phone = models.CharField(max_length=15,null=False)
    address = models.TextField(null=False)
    address_2 = models.TextField(null=False)
    state = models.CharField(max_length=50, null=False)
    district = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    pincode = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    orderstatus = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Completed', 'Completed'),
        ('Order cancelled', 'Order cancelled'),
        ('Returned', 'Returned'),
    )
    status = models.CharField(max_length=200, choices=orderstatus, default='Order confirmed')
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderelate")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
 
    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)

Reasons = (
        ('Recieved wrong Item', 'Recieved wrong Item'),
        ('Damaged Product', 'Damaged Product'),
        ("Don't like the color of the Product", "Don't like the color of the Product"),
        ('Quality of the product not as expected', 'Quality of the product not as expected'),
        ('Product missing in the Packet', 'Product missing in the Packet'),
    )

class Return(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=200)
    comment = models.CharField(max_length=256)
    item_img = models.ImageField(upload_to='photos/return', max_length=256)

    def __unicode__(self):
        return self.Order
