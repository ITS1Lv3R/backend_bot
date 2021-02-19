import requests
from django.contrib import admin
from .models import *


class Project_settingsAdmin(admin.ModelAdmin):
    list_display = ['setting_name', 'setting_int_value']
    list_filter = ['setting_name']


class FnsKeysAdmin(admin.ModelAdmin):
    list_display = ['key', 'response_count', 'active']
    list_filter = ['key', 'response_count', 'active']
    actions = ['update_count']

    def check_limit_key_fns(self, key):
        """Функция для проверки лимата по ключу в сервисе ФНС"""
        # описываем константы для настройки API
        HOST = 'https://api-fns.ru/api/stat'

        params = f'?key={key}'
        url = HOST + params
        response = requests.get(url).json()
        return int(response['Методы']['egr']['Истрачено'])

    def update_count(self, request, queryset):
        """Обновление статистики запросов ключей"""

        for data in queryset:
            data.response_count = self.check_limit_key_fns(data.key)
            if data.response_count >= 100:
                data.active = False
            data.save()

        self.message_user(request, "Записи были обновлены")

    update_count.short_description = 'Обновить статистику запросов'


admin.site.register(Project_settings, Project_settingsAdmin)
admin.site.register(FnsKeys, FnsKeysAdmin)
