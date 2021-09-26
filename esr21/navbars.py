from django.conf import settings
from edc_lab_dashboard.dashboard_urls import dashboard_urls as lab_dashboard_urls
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

esr21.append_item(
    NavbarItem(
        name='esr21_follow',
        title='Follow Ups',
        label='Follow Ups',
        fa_icon='fa-user-plus',
        url_name='esr21_follow:home_url'))

esr21.append_item(
    NavbarItem(
        name='lab',
        label='Specimens',
        fa_icon='fa-flask',
        url_name=lab_dashboard_urls.get('requisition_listboard_url')))

esr21.append_item(
    NavbarItem(
        name='export_data',
        label='Export Data',
        fa_icon='fa fa-database',
        url_name='esr21_export:home_url'))

esr21.append_item(
    NavbarItem(name='synchronization',
               label='Data Synchronization',
               fa_icon='fa-exchange',
               url_name='edc_sync:home_url'))

site_navbars.register(esr21)
