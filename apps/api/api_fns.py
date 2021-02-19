import requests
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.account.models import User, Company
from apps.account.views import check_inn
from apps.main.models import FnsKeys
from django.contrib import messages


@api_view(['POST', ])
@csrf_exempt
def api_to_fns(request):
    """ API для получения данных компании из ФНС и создания карточки предприятия. Необходимо передать параметр "inn" """
    # пытаемся получить данные из запроса
    try:
        user = request.user
        inn = request.data['inn']
        # проверяем, есть ли инн в базе
        if not check_inn(inn):
            return Response({"data_response": "Компания с указанным ИНН уже есть в базе!"},
                            status=status.HTTP_409_CONFLICT)
    except:
        return Response({"data_response": "Необходимо передать параметр 'inn' "}, status=status.HTTP_400_BAD_REQUEST)

    # берём первый активный ключ (активный-значит меньше 100 запросов в месяц)
    try:
        key = FnsKeys.objects.get(active=True)
    except:
        return Response({"data_response": "Нет ни одного активного ключа!"}, status=status.HTTP_400_BAD_REQUEST)

    # настройки для отправки запроса
    HOST = 'https://api-fns.ru/api/egr'
    params = f'?req={inn}&key={key}'
    url = HOST + params

    # отправляем запрос
    response = requests.get(url).json()
    # увеличиваем счетчик запросов ключа
    key.response_count += 1
    key.save()

    # проверяем на пустой ответ
    if not response['items']:
        return Response({"data_response": "Нет компании с таким ИНН в базе ФНС"}, status=status.HTTP_400_BAD_REQUEST)

    # парсим ответ. пока только для ЮЛ
    try:
        if response['items'][0]['ЮЛ']:
            company_type = 'ЮЛ'
    except:
        company_type = 'ИП'
    try:
        company_name_full = response['items'][0]['ЮЛ']['НаимПолнЮЛ']
        company_name_short = response['items'][0]['ЮЛ']['НаимСокрЮЛ']
        company_okopf = response['items'][0]['ЮЛ']['ОКОПФ']
        company_inn = response['items'][0]['ЮЛ']['ИНН']
        company_kpp = response['items'][0]['ЮЛ']['КПП']
        company_ogrn = response['items'][0]['ЮЛ']['ОГРН']
        company_data_reg = response['items'][0]['ЮЛ']['ДатаРег']
        company_director = response['items'][0]['ЮЛ']['Руководитель']['ФИОПолн']
        company_adress = response['items'][0]['ЮЛ']['Адрес']['АдресПолн']
    except:
        pass
    new_company = Company.objects.create(name_full=company_name_full, name_short=company_name_short,
                                         okopf=company_okopf, inn=company_inn, kpp=company_kpp,
                                         ogrn=company_ogrn, ogrn_data_reg=company_data_reg,
                                         director=company_director, adress=company_adress,
                                         user_profile=user, type=company_type)
    new_company.save()
    return Response({"new_company": new_company.name_full}, status=status.HTTP_201_CREATED)


# api_to_fns(5903124140)



