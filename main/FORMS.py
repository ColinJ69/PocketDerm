from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.models import User

class product_form(forms.Form):#The form that starts the scan
    choices = (
        ('General', 'General'),
        ('Aging', 'Aging'),
        ('Acne','Acne'),
        ('Wrinkles', 'Wrinkles'),
        ('Brightening', 'Brightening')
    )
    Concerns = forms.ChoiceField(widget=forms.Select(attrs={'id':'dropdown'}), choices=choices, initial='General', label='')
    
