from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, VendorInfo, BuyerInfo
from django import forms
from .models import Product


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    surname = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    ROLE_CHOICES = (
        #('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'surname', 'address', 'phone_number', 'is_admin', 'is_buyer', 'is_vendor')





class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'description', 'price', 'category', 'image', 'quantity']



class VendorInfoForm(forms.ModelForm):
    class Meta:
        model = VendorInfo
        fields = ()


class BuyerInfoForm(forms.ModelForm):
    class Meta:
        model = BuyerInfo
        fields = ()


