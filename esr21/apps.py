from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


class AppConfig(DjangoAppConfig):
    name = 'esr21'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'AZD 1222'
    institution = 'Botswana-Harvard AIDS Institute'
