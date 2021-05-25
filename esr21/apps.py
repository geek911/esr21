from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig


class AppConfig(DjangoAppConfig):
    name = 'esr21'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'AZD 1222'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = 'botswana'
    definitions = {
        '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[100, 100, 100, 100, 100, 100, 100]),
        '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                             slots=[100, 100, 100, 100, 100])}


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'AZD1222'
    protocol_name = 'ESR21'
    protocol_number = '1222'
    protocol_title = ''
    study_open_datetime = datetime(
        2021, 4, 1, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(
        2025, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))
