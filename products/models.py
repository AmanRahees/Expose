from django.db import models
from category.models import *
from Brand.models import Brand
from django.urls import reverse


# Create your models here.

class SubCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True )
    is_acitve = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategory'

    def __str__(self):
        return self.subcategory_name


class ProductAttribute(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1024, null=True)
    product_offer = models.IntegerField(default=0)
    image = models.ImageField(upload_to='photos/product', max_length=256, null=True, blank=True)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand_name  = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('productDetail', args=[self.category_name, self.slug])

    def __str__(self):
        return self.product_name

class Products(models.Model):
    product_name = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name="productrelate", blank=True, null=True)
    ram = models.ForeignKey(Ram, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=1)
    stock = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __unicode__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Products,related_name="productimg", on_delete=models.CASCADE)
    images = models.ImageField(upload_to='photos/product', max_length=256)

    def __unicode__(self):
        return self.product.product_name