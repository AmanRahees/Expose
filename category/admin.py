from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug', 'Category_img')

class RamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('ram',)}

class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('color',)}

class SizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('size',)}



admin.site.register(Category, CategoryAdmin)
admin.site.register(Ram, RamAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
