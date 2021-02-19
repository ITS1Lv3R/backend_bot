from rest_framework import serializers

from apps.account.models import User
from apps.main.models import Project_settings


class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для пользователей"""

    class Meta:
        model = User
        fields = '__all__'  # пока отдаём все поля, нужно будет указать конкретные


class ProjectSettingsSerializer(serializers.ModelSerializer):
    """ Сериалайзер для настроек проекта"""

    class Meta:
        model = Project_settings
        fields = '__all__'
