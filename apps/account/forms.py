from django import forms
from .models import User


class LoginForm(forms.Form):
    """Класс для формы авторизации на сайте"""
    user_phone = forms.CharField(label='Номер телефона')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    """Класс для формы личного кабинета"""

    class Meta:
        model = User
        fields = ('email', 'user_phone', 'user_inn', 'user_role')


class UserRegistrationForm(UserProfileForm):
    """Класс для формы регистрации на сайте"""
    # Наследуемся от класса профиля, чтобы добавить в регистрацию пароль
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
