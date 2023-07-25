from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=1024, blank=True)
    category_offer = models.IntegerField(default=0, blank=True)
    Category_img = models.ImageField(upload_to='photos/Category', blank=True)
    is_active = models.BooleanField(default=True) 

    class Meta: 
        verbose_name = 'catergory'
        verbose_name_plural = 'categories'

    def get_url(self):
         return reverse('by_category',args=[self.slug])


    def __str__(self):
        return self.category_name


class Ram(models.Model):
    ram = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    is_acitve = models.BooleanField(default=True)

    def __str__(self):
        return self.ram



class Color(models.Model):
    color = models.CharField(max_length=200)
    color_code  = models.CharField(max_length = 100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True) 
    is_acitve = models.BooleanField(default=True)

    def __str__(self):
        return self.color