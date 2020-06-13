from django import forms
from .models import Payment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['name', 'surname', 'address']
