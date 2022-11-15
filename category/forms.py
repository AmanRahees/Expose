from django import forms
from .models import Category
from django.forms import widgets

class AddCategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ["category_name","slug","description","Category_img"]
    widgets = {
      'category_name': forms.TextInput(attrs={'class':'form-control'}),
      'slug': forms.TextInput(attrs={'class':'form-control'}),
      'description': forms.Textarea(attrs={'class':'form-control'}),
      'Category_img': forms.ClearableFileInput(attrs={'class':'form-control'}),
    }

class EditCategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ["category_name","slug","description","Category_img"]