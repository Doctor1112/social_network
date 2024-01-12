from typing import Any
from django import forms
from .models import UserProfile
from allauth.account.forms import SignupForm, LoginForm
from django.forms import CharField, ModelForm


class UserSignupForm(SignupForm):
    first_name = CharField(max_length=100, required=True, label="Имя")
    last_name = CharField(max_length=100, required=True, label="Фамилия")

# class LoginForm(LoginForm):
    

    




    
