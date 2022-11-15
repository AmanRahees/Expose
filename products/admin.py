from django.contrib import admin
from .models import SubCategory, Products, Variation

# Register your models here.

class SubCategoryAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':('subcategory_name',)}

class ProductAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':('product_name',)}
   list_display = ('product_name','product_brand','product_category','modified_date','is_available')



admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Products,ProductAdmin)
admin.site.register(Variation)