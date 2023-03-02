from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=3)
    password1 = forms.CharField(widget=forms.PasswordInput(), min_length=5,
                                max_length=15)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=5,
                                max_length=15)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5,
                               max_length=15)