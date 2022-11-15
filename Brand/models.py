from django.db import models

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200)
    Brand_img = models.ImageField(upload_to='photos/brand', blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.brand_name