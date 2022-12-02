from django.contrib import admin
from .models import *
# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('brand_name',)}
    list_display = ('brand_name','slug', 'Brand_img')

admin.site.register(Brand, BrandAdmin)
admin.site.register(Coupon)
