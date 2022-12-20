from django import forms
from .models import *

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name","last_name","email","phone_number"]
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number':forms.NumberInput(attrs={'class':'form-control'}),
        }

class AddImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_img"]
        widgets = {
            'phone_number':forms.FileInput(attrs={'class':'form-control'}),
        }