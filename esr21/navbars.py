from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar

esr21 = Navbar(name='esr21')

esr21.append_item(
    NavbarItem(
        name='eligible_subject',
        label='Subject Screening',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')))

esr21.append_item(
    NavbarItem(
        name='consented_subject',
        label='Subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES.get('subject_listboard_url')))

# esr21.append_item(
    # NavbarItem(name='synchronization',
               # label='Data Synchronization',
               # fa_icon='fa-exchange',
               # url_name='edc_sync:home_url'))

site_navbars.register(esr21)
