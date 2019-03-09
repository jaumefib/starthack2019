from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.CharField(max_length=30, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
