from django.contrib.auth.models import UserManager
from django.db import models


class Project_settings(models.Model):
    """ Модель для хранения кастомных настроек проекта"""
    setting_name = models.CharField(max_length=255, verbose_name='Наименование настройки', blank=True)
    setting_int_value = models.IntegerField(verbose_name='Значение настройки (число)', default=0, null=True, blank=True)
    objects = UserManager()

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return self.setting_name


class FnsKeys(models.Model):
    """ Модель для хранения ключей fns"""
    key = models.CharField(max_length=255, verbose_name='Наименование ключа')
    response_count = models.IntegerField(verbose_name='Потрачено запросов в месяц', default=0, null=True)
    active = models.BooleanField(verbose_name='Активность ключа',
                                 default=True)  # ключ ограничен 100 запросами в месяц, флаг для деактивации ключа

    objects = UserManager()

    class Meta:
        verbose_name = 'Ключ ФНС'
        verbose_name_plural = 'Ключи ФНС'

    def __str__(self):
        return self.key
