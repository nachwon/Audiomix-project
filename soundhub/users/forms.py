from django import forms


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
