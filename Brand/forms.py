from django import forms
from .models import *


class AddBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["brand_name","slug","Brand_img"]
        widgets = {
            'brand_name':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            'Brand_img':forms.ClearableFileInput(attrs={'class':'form-control'})
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ["code","offer_value","valid_at","active"]
        widgets = {
            'code':forms.TextInput(attrs={'class':'form-control text-light'}),
            'offer_value':forms.NumberInput(attrs={'class':'form-control text-light'}),
            'valid_at': DateInput(attrs={'class':'form-control w-25 text-light'}),
            'active':forms.CheckboxInput(),
        }

class EditCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ["offer_value","valid_at","active"]
        widgets = {
            'offer_value':forms.NumberInput(attrs={'class':'form-control text-light'}),
            'valid_at': DateInput(attrs={'class':'form-control w-25 text-light'}),
        }