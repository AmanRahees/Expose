from django import forms
from django.forms import widgets
from .models import *


class AddProductAttributeForm(forms.ModelForm):
  class Meta:
    model = ProductAttribute
    fields = ["product_name","slug","description","image","image_2","image_3","category_name","subcategory_name","brand_name","is_active"]
    widgets = {
      'product_name':forms.TextInput(attrs={'class':'text-light form-control'}),
      'slug':forms.TextInput(attrs={'class':'text-light form-control'}),
      'description': forms.Textarea(attrs={'class':'form-control'}),
      'image': forms.FileInput(attrs={'class':'form-control'}),
      'image_2': forms.FileInput(attrs={'class':'form-control'}),
      'image_3': forms.FileInput(attrs={'class':'form-control'}),
      'category_name':forms.Select(attrs={'class':'text-light form-control', 'onchange' : "getsub(this);"}),
      'subcategory_name':forms.Select(attrs={'class':'text-light form-control'}),
      'brand_name':forms.Select(attrs={'class':'text-light form-control'}),
      'is_acitve':forms.CheckboxInput()
    }


class EditProductAttributeForm(forms.ModelForm):
  class Meta:
      model = ProductAttribute
      fields = ["product_name","slug","description","image"]
      widgets = {
        'product_name':forms.TextInput(attrs={'class':'text-light form-control'}),
        'slug':forms.TextInput(attrs={'class':'text-light form-control'}),
        'description': forms.Textarea(attrs={'class':'form-control'}),
        'image': forms.FileInput(attrs={'class':'form-control'}),
        'image_2': forms.FileInput(attrs={'class':'form-control'}),
        'image_3': forms.FileInput(attrs={'class':'form-control'}),
      }


class AddSubCategoryForm(forms.ModelForm):
  class Meta:
    model = SubCategory
    fields = ["category_name","subcategory_name","slug","is_acitve"]
    widgets = {
      'category_name':forms.Select(attrs={'class':'text-light form-control'}),
      'subcategory_name':forms.TextInput(attrs={'class':'text-light form-control'}),
      'slug':forms.TextInput(attrs={'class':'text-light form-control'}),
      'is_acitve':forms.CheckboxInput()
    }

class EditSubCategoryForm(forms.ModelForm):
  class Meta:
    model = SubCategory
    fields = ["subcategory_name","slug"]


class AddProductForm(forms.ModelForm):
  class Meta:
    model = Products
    fields = ["product_name","ram","color","price","stock","is_available"]
    widgets = {
      'product_name': forms.Select(attrs={'class':'form-control text-light'}),
      'ram': forms.Select(attrs={'class':'form-control text-light'}),
      'color': forms.Select(attrs={'class':'form-control text-light'}),
      'price': forms.NumberInput(attrs={'class':'text-light form-control active'}),
      'stock': forms.NumberInput(attrs={'class':'text-light form-control'}),
      'is_available':forms.CheckboxInput()
    }


class EditProductForm(forms.ModelForm):
    class Meta:
      model = Products
      fields = ["price","stock"]