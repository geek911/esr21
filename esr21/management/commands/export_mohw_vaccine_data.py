
from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from edc_base.utils import get_utcnow

import pandas as pd


class Command(BaseCommand):

    help = 'Export Vaccine data'

    personal_contact_info_model = 'esr21_subject.personalcontactinfo'
    demographics_data_model = 'esr21_subject.demographicsdata'
    informed_consent_model = 'esr21_subject.informedconsent'
    vaccination_details_model = 'esr21_subject.vaccinationdetails'
    registered_subject_model = 'edc_registration.registeredsubject'
    covid19_results_model = 'esr21_subject.covid19results'
    screening_eligibility_model = 'esr21_subject.screeningeligibility'
    medical_history_model = 'esr21_subject.medicalhistory'
    pregnancy_model = 'esr21_subject.pregnancytest'

    @property
    def personal_contact_info_cls(self):
        return django_apps.get_model(self.personal_contact_info_model)

    @property
    def demographics_data_cls(self):
        return django_apps.get_model(self.demographics_data_model)

    @property
    def informed_consent_cls(self):
        return django_apps.get_model(self.informed_consent_model)

    @property
    def vaccination_details_cls(self):
        return django_apps.get_model(self.vaccination_details_model)

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)

    @property
    def covid19_results_cls(self):
        return django_apps.get_model(self.covid19_results_model)

    @property
    def medical_history_cls(self):
        return django_apps.get_model(self.medical_history_model)

    @property
    def pregnancy_cls(self):
        return django_apps.get_model(self.pregnancy_model)

    def add_arguments(self, parser):
        parser.add_argument(
            'site_id', type=str, help='Site specific export')

    def district_check(self, location):
        location = location.lower()
        switcher = {
            'gaborone': 'South East',
            'maun': 'Ngamiland',
            'francistown': 'North East',
            'phikwe': 'Central',
            'serowe': 'Central',
        }
        return switcher.get(location, 'no location')

    def site_name_by_id(self, site_id=None):
        sites_mapping = {
            '40': 'gaborone',
            '41': 'maun',
            '42': 'serowe',
            '43': 'francistown',
            '44': 'phikwe'}
        return sites_mapping.get(site_id, site_id)

    def dosage_mapping(self, dose_type=None):
        dosage_mapping = {
            'first_dose': 'DOSE1',
            'second_dose': 'DOSE2',
            'booster_dose': 'BOOSTER DOSE'}
        return dosage_mapping.get(dose_type, '')

    def handle(self, *args, **kwargs):
        identifiers = []
        site_id = kwargs.get('site_id')

        if site_id == 'all':
            identifiers = self.registered_subject_cls.objects.values_list(
                'subject_identifier', flat=True)
        else:
            identifiers = self.registered_subject_cls.objects.filter(
                site_id=site_id).values_list('subject_identifier', flat=True)

        vaccinations_tuple = ('received_dose_before', 'vaccination_site',
                              'vaccination_date', 'site', 'lot_number')

        count = 0
        toCSV = []
        for identifier in identifiers[:6]:
            obj_dict = {}

            consent = self.informed_consent_cls.objects.filter(
                subject_identifier=identifier).last()
            if not consent:
                continue
            first_name = consent.first_name
            last_name = consent.last_name
            dob = consent.dob
            gender = consent.get_gender_display()
            age = consent.formatted_age_at_consent
            country = None
            employment_status = None
            employment_status_other = None
            subject_cell = None
            physical_address = None
            location = None
            district = None
            occupation = None
            covid19_results = None
            employer = None
            comorbidities = None
            pregnancy_test = None

            identity_number = consent.identity

            demographics = self.demographics_data_cls.objects.filter(
                subject_visit__subject_identifier=identifier).last()
            if demographics:
                country = demographics.country
                employment_status = demographics.get_employment_status_display()
                employment_status_other = demographics.employment_status_other
                if employment_status_other:
                    occupation = employment_status_other
                else:
                    occupation = employment_status

            try:
                personal_contact = self.personal_contact_info_cls.objects.get(
                    subject_identifier=identifier)
            except self.personal_contact_info_cls.DoesNotExist:
                pass
            else:
                subject_cell = personal_contact.subject_cell
                physical_address = personal_contact.physical_address
                employer = personal_contact.subject_work_place

            try:
                covid19 = self.covid19_results_cls.objects.get(subject_visit__subject_identifier=identifier)
            except self.covid19_results_cls.DoesNotExist:
                pass
            else:
                covid19_results = covid19.covid_result

            try:
                medical_history = self.medical_history_cls.objects.get(subject_visit__subject_identifier=identifier)
            except self.medical_history_cls.DoesNotExist:
                pass
            else:
                comorbidities = medical_history.comorbidities.all()
                comorbidities = [commorbidity.name for commorbidity in comorbidities if commorbidity.name != 'Not Applicable']

            try:
                pregnancy = self.pregnancy_cls.objects.filter(subject_visit__subject_identifier=identifier).latest('created')
            except self.pregnancy_cls.DoesNotExist:
                pass
            else:
                pregnancy_test = pregnancy.result

            obj_dict.update(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                dob=dob,
                age=age,
                subject_cell=subject_cell,
                identity_number=identity_number,
                covidzone=f'Greater {location} Zone',
                physical_address=physical_address,
                occupation=occupation,
                nationality=country,
                identity_type=consent.identity_type,
                employer=employer,
                covid19_results=covid19_results,
                comorbidities=comorbidities,
                pregnancy_test=pregnancy_test)

            vaccinations = self.vaccination_details_cls.objects.filter(
                received_dose='Yes',
                subject_visit__subject_identifier=identifier).only(*vaccinations_tuple)

            vaccine_type = 'Astra-Zeneca'
            for vaccination in vaccinations:
                dose_type = self.dosage_mapping(dose_type=vaccination.received_dose_before)

                # Get vaccination disctrict from site name
                site = vaccination.site.name
                location = site[6:]
                district = self.district_check(location)

                obj_dict.update(
                    {f'{dose_type}_vaccinesite': vaccination.vaccination_site,
                     f'{dose_type}_vaccine_type': vaccine_type,
                     f'{dose_type}_district': district,
                     f'{dose_type}_date_vaccinated': vaccination.vaccination_date,
                     f'{dose_type}_BatchNumber': vaccination.lot_number,
                     f'{dose_type}_Expirydate': vaccination.expiry_date, })

            toCSV.append(obj_dict)
            count += 1

        df = pd.DataFrame(toCSV)
        df_mask = df.copy()
        df_mask2 = df_mask.rename(
            columns={'first_name': 'Firstname',
                     'last_name': 'Surname',
                     'gender': 'Sex',
                     'dob': 'Date of Birth',
                     'subject_cell': 'Mobile Number',
                     'identity_number': 'Identity Number',
                     'pregnancy_test': 'Pregnancy',
                     'covid19_results': 'Have you tested positive for covid 19',
                     'covidzone': 'Covid Zone',
                     'district': 'District',
                     'physical_address': 'Address',
                     'occupation': 'Occupation',
                    })

        timestamp = get_utcnow().strftime("%m%d%Y%H%M%S")
        site_name = self.site_name_by_id(site_id=site_id)
        df_mask2.to_csv(f'~/source/esr21/{site_name}_vaccinations_{timestamp}.csv', index=False)
        # with open('vacinations_' + timestamp + '.csv', 'w', newline='')  as output_file:
        #     dict_writer = csv.DictWriter(output_file)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(df_mask2)
        self.stdout.write(self.style.SUCCESS(f'Total exported: {count}.'))
