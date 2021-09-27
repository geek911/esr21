from django.views.generic import TemplateView
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'esr21/home.html'
    navbar_name = 'esr21'
    navbar_selected_item = 'home'

    vaccine_model = 'esr21_subject.vaccinationdetails'
    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    subject_consent_model = 'esr21_subject.informedconsent'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def vaccine_model_cls(self):
        return django_apps.get_model(self.vaccine_model)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_screening = self.subject_screening_cls.objects.all()
        subject_consent = self.subject_consent_cls.objects.all()
        vaccinated_first_dose = self.vaccine_model_cls.objects.filter(
            received_dose='Yes', received_dose_before='first_dose')
    
        vaccinated_second_dose = self.vaccine_model_cls.objects.filter(
            received_dose='Yes', received_dose_before='second_dose')

        screened_subjects = subject_screening.count()
        consented_subjects = subject_consent.count()
        vaccinated_first_dose = vaccinated_first_dose.count()
        vaccinated_second_dose = vaccinated_second_dose.count()

        context.update(
            vaccinated_first_dose=vaccinated_first_dose,
            vaccinated_second_dose=vaccinated_second_dose,
            consented_subjects=consented_subjects,
            screened_subjects=screened_subjects)

        return context
