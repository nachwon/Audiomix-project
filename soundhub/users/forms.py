from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


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


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'signup-field transition',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'signup-field transition',
            'placeholder': 'Password Confirmation'
        }))

    class Meta:
        model = User
        fields = (
            'email',
            'nickname',
            'password1',
            'password2',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'signup-field transition',
                    'placeholder': 'E-mail Address',
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'class': 'signup-field transition',
                    'placeholder': 'Nickname',
                }
            ),
        }
