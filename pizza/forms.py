from django import forms
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'surname', 'address']
