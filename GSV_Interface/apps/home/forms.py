# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post

class PostForm(forms.Form):
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Adress",
                "class": "form-control"
            }
        ))
    yearInput = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Year",
                "class": "form-control"
            }
        ))


    class Meta:
        model = Post
        fields = ('address','year')
