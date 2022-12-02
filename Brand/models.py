from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import utc
import datetime

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200)
    brand_offer = models.IntegerField(default=0)
    Brand_img = models.ImageField(upload_to='photos/brand', blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

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


    