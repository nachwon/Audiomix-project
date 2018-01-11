from django import forms


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=255,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'signin-field',
                                 }
                             ))
    password = forms.CharField(widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'signin-field'
                                   }
                               ))
