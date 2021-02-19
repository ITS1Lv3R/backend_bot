import requests
from django.contrib import admin
from .models import User, Company
from ..main.models import FnsKeys


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'user_role', 'user_phone', 'user_inn', 'is_active', 'is_confirmed', 'date_joined']
    list_filter = ['email', 'user_role', 'user_phone', 'user_inn', 'is_active', 'is_confirmed', 'date_joined']
    actions = ['update_profile']

    def update_profile(self, request, queryset):
        queryset.update(email='test@test.ru')
        self.message_user(request, "Записи были обновлены")

    update_profile.short_description = 'Обновить профиль'


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name_full', 'user_profile', 'inn', 'kpp', 'ogrn', 'ogrn_data_reg']
    list_filter = ['name_full', 'user_profile', 'inn', 'kpp', 'ogrn', 'ogrn_data_reg']
    actions = ['update_info']

    def update_info(self, request, queryset):
        """Обновление информации по компаниям"""
        HOST = 'https://api-fns.ru/api/egr'
        # берём первый активный ключ (активный-значит меньше 100 запросов в месяц)
        key = FnsKeys.objects.get(active=True)
        for company in queryset:
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

        self.message_user(request, "Записи были обновлены")

    update_info.short_description = 'Обновить информацию'


admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
