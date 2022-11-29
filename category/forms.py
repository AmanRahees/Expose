from django import forms
from .models import *
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

class AddRamForm(forms.ModelForm):
  class Meta:
    model = Ram
    fields = ["ram","slug","is_acitve"]
    widgets={
      'ram' : forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'slug': forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'is_acitve': forms.CheckboxInput()
    }

class AddColorForm(forms.ModelForm):
  class Meta:
    model = Color
    fields = ["color","slug","color_code","is_acitve"]
    widgets={
      'color' : forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'slug': forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'color_code': forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'is_acitve': forms.Select(attrs={'class':'form-control w-75 text-light'}),
    }

class AddSizeForm(forms.ModelForm):
  class Meta:
    model = Size
    fields = ["size","slug","is_acitve"]
    widgets={
      'size' : forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'slug': forms.TextInput(attrs={'class':'form-control w-75 text-light'}),
      'is_acitve': forms.CheckboxInput()
    }