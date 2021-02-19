import requests
from celery import shared_task

from apps.account.models import Company
from apps.main.models import FnsKeys


@shared_task
def check_limit_key_fns():
    """Задача CELERY для проверки лимата по ключу в сервисе ФНС"""
    # описываем константы для настройки API
    HOST = 'https://api-fns.ru/api/stat'

    keys = FnsKeys.objects.all()
    for key in keys:
        params = f'?key={key}'
        url = HOST + params
        response = requests.get(url).json()
        key.response_count = int(response['Методы']['egr']['Истрачено'])
        if key.response_count >= 100:
            key.active = False
        key.save()
        return key.key


@shared_task
def api_to_fns_update():
    """ Задача CELERY для обновления информации по компаниями"""
    HOST = 'https://api-fns.ru/api/egr'
    # берём первый активный ключ (активный-значит меньше 100 запросов в месяц)
    key = FnsKeys.objects.get(active=True)
    companies = Company.objects.all()
    for company in companies:
        inn = company.inn
        params = f'?req={inn}&key={key}'
        url = HOST + params
        # отправляем запрос
        response = requests.get(url).json()
    # увеличиваем счетчик запросов ключа
        key.response_count += 1
        key.save()
    # обновляем данные компании
        company.name_full = response['items'][0]['ЮЛ']['НаимПолнЮЛ']
        company.name_short = response['items'][0]['ЮЛ']['НаимСокрЮЛ']
        company.company_okopf = response['items'][0]['ЮЛ']['ОКОПФ']
        company.inn = response['items'][0]['ЮЛ']['ИНН']
        company.kpp = response['items'][0]['ЮЛ']['КПП']
        company.ogrn = response['items'][0]['ЮЛ']['ОГРН']
        company.ogrn_data_reg = response['items'][0]['ЮЛ']['ДатаРег']
        company.director = response['items'][0]['ЮЛ']['Руководитель']['ФИОПолн']
        company.adress = response['items'][0]['ЮЛ']['Адрес']['АдресПолн']
        company.save()
        return company.name_full


