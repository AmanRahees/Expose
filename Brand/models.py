from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import utc
from accounts.models import *
from django.urls import reverse

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200)
    Brand_img = models.ImageField(upload_to='photos/brand', null=False)
    is_available = models.BooleanField(default=True)

    class Meta: 
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def brnd_get_url(self):
         return reverse('by_brand',args=[self.slug])

    def __str__(self):
        return self.brand_name

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    offer_value = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(20)],  null=False)
    valid_from = models.DateTimeField(auto_now_add=True, null=True)
    valid_at = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def get_absolute_url(self): 
        return reverse('couponshow')

class Couponuser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon_model = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True, related_name='cpnrrelate')
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    coupon_value = models.IntegerField(null=True, blank=True)
    used = models.BooleanField(default=False)