from django import forms
from .models import Brand


class AddBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["brand_name","slug","Brand_img"]
        widgets = {
            'brand_name':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            'Brand_img':forms.ClearableFileInput(attrs={'class':'form-control'})
        }