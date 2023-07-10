from django.contrib.auth.forms import UserCreationForm
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ResetPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Пользователя с таким email не существует!")
        return email
