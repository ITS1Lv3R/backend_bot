from django import forms


class ConfigurationForm(forms.Form):
    """Форма для конфигурации системы из админ.панели"""
    demo_session_live_param = forms.IntegerField(label='Время демо-сессии')
