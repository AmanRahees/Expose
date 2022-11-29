from django.contrib import admin
from .models import *

# Register your models here.
class ProductImageInline(admin.TabularInline):
   model = ProductImage
   extra = 1
   

class SubCategoryAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':('subcategory_name',)}

class ProductAttributeAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':('product_name',)}

class ProductAdmin(admin.ModelAdmin):
   model = Products
   list_display = ('id' , 'product_name')
   inlines = (ProductImageInline,)
   

admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(ProductImage)
