import random
import json

import requests
from django.core.exceptions import EmptyResultSet
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from rest_framework.decorators import api_view, renderer_classes
from django.core.mail import EmailMessage
from rest_framework.renderers import JSONRenderer

from .serializers import UserSerializer, ProjectSettingsSerializer
from .smsc_api import SMSC
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import User, Company

from ..main.models import Project_settings


@api_view(['POST', ])
@csrf_exempt
def api_sending_sms(request):
    """Отправка смс пользователю с 6-значным кодом, необходимо передать параметр 'user_phone' """
    data_response = {'user_phone': 'Invalid Data'}
    if request.method == 'POST':
        # Пробуем получить значение параметра user_phone
        try:
            user_phone = request.data['user_phone']
        except:
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
        sms_code = random.randint(99999, 999999)
        smsc = SMSC()

        # пробуем отправить смс пользователю
        try:
            smsc.send_sms(phones=user_phone, message=str(sms_code), sender="config")
        except:
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)
        # если всё ок, возвращаем код в смс на фронт
        return Response({'sms_code': str(sms_code)}, status.HTTP_200_OK)
    else:
        return Response(data_response, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    """ Класс для работы с моделью Пользователя"""
    # добавлям пустые списки, чтобы не ругался csrf
    permission_classes = ()
    authentication_classes = ()

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectSettingsViewSet(viewsets.ModelViewSet):
    """ Класс для вьюссета настроек проекта"""
    queryset = Project_settings.objects.all()
    serializer_class = ProjectSettingsSerializer


def send_mail(request):
    """ Тестовая функция отправки email с настройками SMTP яндекса"""
    subject_pay = 'Авторизация нового пользователя'
    mail_from = 'no-reply@config.net'
    mail_to = ['john_k@inbox.ru', ]
    admin_message = 'Тест'
    mail = EmailMessage(subject_pay, admin_message, mail_from, mail_to)
    mail.content_subtype = "html"
    mail.send()
    return redirect('main:index')


@api_view(('GET',))
def check_user_auth(request):
    """ API проверки авторизации юзера"""
    if request.user.is_authenticated:
        return Response({'auth': True}, status.HTTP_200_OK)
    else:
        return Response({'auth': False}, status.HTTP_200_OK)
