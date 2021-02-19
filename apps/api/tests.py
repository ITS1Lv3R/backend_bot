# from smsc_api  import SMSC
#
# smsc = SMSC()
#
# r = smsc.send_sms("89124808959", "Тест", sender="config")
#


import requests


def api_to_fns(inn):

    host = 'https://api-fns.ru/api/egr'
    key = 'e01f2291d55b8429774ffffbe148a2426b6a8a4c'

    params = f'?req={inn}&key={key}'

    url = host + params

    response = requests.get(url).json()

    if response['items'] == []:
        print('нет компании')

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


    print(response)

api_to_fns(5903124141)

# # api_to_fns(591907595850) 5903124140


# def check_limit_key_fns(key):
#     """Функция для проверки лимата по ключу в сервисе ФНС"""
#     # описываем константы для настройки API
#     HOST = 'https://api-fns.ru/api/stat'
#     params = f'?key={key}'
#     url = HOST + params
#
#     response = requests.get(url).json()
#     response_count = response['Методы']['egr']['Истрачено']
#     print(response_count)
#
#
# check_limit_key_fns(key='e01f2291d55b8429774ffffbe148a2426b6a8a4c')
