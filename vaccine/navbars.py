from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar

vaccine = Navbar(name='vaccine')

# vaccine.append_item(
    # NavbarItem(
        # name='eligible_subject',
        # label='Eligibility Checklist',
        # fa_icon='fa-user-plus',
        # url_name=settings.DASHBOARD_URL_NAMES.get('eligibility_listboard_url')))
        #
# vaccine.append_item(
    # NavbarItem(
        # name='vaccine_subject',
        # label='Subjects',
        # fa_icon='far fa-user-circle',
        # url_name=settings.DASHBOARD_URL_NAMES.get('subject_listboard_url')))

# vaccine.append_item(
    # NavbarItem(name='synchronization',
               # label='Data Synchronization',
               # fa_icon='fa-exchange',
               # url_name='edc_sync:home_url'))

site_navbars.register(vaccine)
