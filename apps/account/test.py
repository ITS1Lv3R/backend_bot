import os

import django
from django.conf import settings


settings.configure(
    INSTALLED_APPS=[
        'account',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'main',
        'api',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
        }
    })

django.setup()

import random
from django.core.mail import EmailMessage


def mail_to_activate_account(user_mail):
    code = random.randint(99999, 999999)
    message_theme = 'Подтверждение email'
    mail_from = 'john_k@inbox.ru'
    mail_to = [user_mail]
    message = 'Код верификации:{} <br> ' \
              'Введите код в форме регистрации на сайте'.format(code)

    mail = EmailMessage(message_theme, message, mail_from, mail_to)
    mail.content_subtype = "html"
    mail.send()




