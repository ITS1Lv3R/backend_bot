from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import User, Company
from django.contrib.auth import logout
from apps.main.models import Project_settings


def user_login(request):
    """Функция для авторизации юзера"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():  # Проверяем форму на валидность
            cd = form.cleaned_data
            user = authenticate(user_phone=cd['user_phone'],
                                password=cd['password'])
            if user:  # Проверяем есть ли юзер в бд
                if user.is_active:  # Проверяем активен ли юзер
                    login(request, user)
                    messages.success(request, 'Вы успешно авторизовались на сайте!')
                    return redirect('main:index')  # Если всё ок, отправляем юзера на главную страницу
                else:
                    messages.error(request, 'Аккаунт неактивен!')
                    context = locals()
                    template = 'account/login.html'
                    return render(request, template, context)
            else:
                messages.error(request, 'Неверные логин или пароль')
                context = locals()
                template = 'account/login.html'
                return render(request, template, context)
    else:
        form = LoginForm()
    context = locals()
    template = 'account/login.html'
    return render(request, template, context)


def user_logout(request):
    """Функция для логаута"""
    logout(request)
    template = 'account/logged_out.html'
    return render(request, template)


def make_session_not_permanent(request):
    """ Функция для демо-доступа"""
    # Устанавливаем доступ пользователю на определенное количество секунд
    demo_session_live_param = Project_settings.objects.get(setting_name='demo_session_live_param')
    request.session.set_expiry(demo_session_live_param)
    return redirect('main:index')


def register(request):
    """Функция для регистрации юзера"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # проверяем на валидность форму юзера
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user_phone = user_form.cleaned_data["user_phone"]
            new_user.set_password(user_form.cleaned_data['password'])
            new_user_email = user_form.cleaned_data["email"]
            new_user_role = user_form.cleaned_data["user_role"]
            new_user_inn = user_form.cleaned_data["user_inn"]
            # если валидна, то создаём юзера
            new_user.save()
            # После создания юзера и профиля отправляем пользователя на главную страницу
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрированы на сайте!')
            # messages.success(request, 'На указанный Вами почтовый адрес отправлено письмо с сылкой на '
            #                           'активацию аккаунта. Пожалуйста, подтвердите, почтовый адрес')
            # # Отправляем письмо с активацией
            # mail_to_activate_account(new_user_email)
            return redirect('main:index')
        else:
            context = locals()
            template = 'account/register.html'
            return render(request, template, context)

    else:
        user_form = UserRegistrationForm()
    context = locals()
    template = 'account/register.html'
    return render(request, template, context)


@login_required
def profile(request):
    """Функция личного кабинета"""
    # блок для редактирования профиля
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш Профиль успешно изменён')
    else:
        user_form = UserProfileForm(instance=request.user)
    context = locals()
    template = 'account/profile.html'
    return render(request, template, context)


def mail_to_activate_account(email):
    """Отправка письма Пользователю после регистрации"""
    message_theme = 'Подтверждение email'
    mail_from = 'john_k@inbox.ru'
    mail_to = [email]
    message = 'Пройдите по ссылке ниже для подверждения аккаунта: <br> {} ' \
              ''.format('<a href="localhost:8000/account/activate/{}">Подтверждение</a>').format(email)

    mail = EmailMessage(message_theme, message, mail_from, mail_to)
    mail.content_subtype = "html"
    mail.send()


def activate_account(request, email):
    """ Активация аккаунта Пользователя после прохождения по ссылке"""
    user = User.objects.get(email=email)
    if user.is_confirmed:
        messages.error(request, 'Аккаунт не нуждается в активации')
    else:
        user.is_confirmed = True
        user.save()
        messages.success(request, 'Аккаунт активирован')
        return redirect('main:index')


def check_inn(inn):
    """ Функция для проверки инн в базе"""

    if Company.objects.filter(inn=inn).exists():
        return False
    else:
        return True
