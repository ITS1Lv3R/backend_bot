from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ConfigurationForm

from django.db.models import Q

from ..account.models import User


class UserphoneOrEmailBackend(object):
    """ Переоопределяем бэкэнд для авторизации по номеру телефона или email"""

    def authenticate(self, user_phone=None, password=None, **kwargs):
        try:
            # Try to fetch the user by searching the username or email field
            user = User.objects.get(Q(user_phone=user_phone) | Q(email=str(user_phone)))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)


def index(request):
    template = 'main/index.html'
    return render(request, template)


def page_not_found(request, exception):
    template = 'main/404.html'
    status = 404
    context = locals()
    return render(request, template, context)


def page_not_found_500(request):
    template = 'main/500.html'
    status = 500
    context = locals()
    return render(request, template, context)
