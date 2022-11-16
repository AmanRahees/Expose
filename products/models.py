from django.db import models
from category.models import Category
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


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=1024, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    Product_img = models.ImageField(upload_to='photos/Products')
    Product_img2 = models.ImageField(upload_to='photos/Products', help_text=("Not Required"), blank=True)
    Product_img3 = models.ImageField(upload_to='photos/Products',help_text=("Not Required"), blank=True)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('productDetail', args=[self.product_category.slug, self.slug])


    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def memorys(self):
        return super(VariationManager, self).filter(variation_category='memory', is_acitve=True)

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_acitve=True)

Variation_Category = (
    ('memory','memory'),
    ('color','color')
)


class Variation(models.Model):
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=Variation_Category)
    variation_value = models.CharField(max_length=200)
    is_acitve = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    class Meta:
        verbose_name = 'variation'
        verbose_name_plural = 'variations'

    def __str__(self):
        return self.variation_value