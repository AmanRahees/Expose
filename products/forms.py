from django import forms
from django.forms import widgets
from .models import *

class AddProductForm(forms.ModelForm):
  class Meta:
    model = Products
    fields = ["product_name","slug","description","price","stock","Product_img","Product_img2","Product_img3","product_category","product_subcategory","product_brand","is_available"]
    widgets = {
      'product_name': forms.TextInput(attrs={'class':'form-control'}),
      'slug': forms.TextInput(attrs={'class':'form-control'}),
      'description': forms.Textarea(attrs={'class':'form-control'}),
      'price': forms.NumberInput(attrs={'class':'text-light form-control active'}),
      'stock': forms.NumberInput(attrs={'class':'text-light form-control'}),
      'Product_img': forms.ClearableFileInput(attrs={'class':'form-control'}),
      'Product_img2': forms.ClearableFileInput(attrs={'class':'form-control'}),
      'Product_img3': forms.ClearableFileInput(attrs={'class':'form-control'}),
      'product_category': forms.Select(attrs={'class':'text-light form-control'}),
      'product_subcategory': forms.Select(attrs={'class':'text-light form-control'}),
      'product_brand': forms.Select(attrs={'class':'text-light form-control'}),
      'is_available':forms.CheckboxInput()
    }


class EditProductForm(forms.ModelForm):
    class Meta:
      model = Products
      fields = ["product_name","slug","description","price","stock","Product_img","Product_img2","Product_img3"]

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


class AddVariationForm(forms.ModelForm):
  class Meta:
    model = Variation
    fields = ['product_name','variation_category','variation_value','is_acitve']
    widgets = {
      'product_name': forms.Select(attrs={'class':'text-light form-control'}),
      'variation_category': forms.Select(attrs={'class':'text-light form-control'}),
      'variation_value': forms.TextInput(attrs={'class':'text-light form-control'}),
      'is_acitve':forms.CheckboxInput()
    }

class EditVariationForm(forms.ModelForm):
    class Meta:
      model = Variation
      fields = ['variation_value']