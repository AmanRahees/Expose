from django import forms
from .models import  *


class AddAddressform(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Name'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Phone Number'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    district = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = useraddress
        fields = ['user_id','name', 'address', 'address_2', 'city', 'district', 'state', 'pincode', 'mobile', 'email']


class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = useraddress
        fields=['name','mobile','email','address','address_2','city','district','state', 'pincode']


class OrderStatus(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']
