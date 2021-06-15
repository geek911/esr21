from django.views.generic import TemplateView
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'esr21/home.html'
    navbar_name = 'esr21'
    navbar_selected_item = 'home'

    enrollment_model = 'esr21_subject.informedconsent'
    subject_screening_model = 'esr21_subject.eligibilityconfirmation'
    subject_consent_model = 'esr21_subject.informedconsent'

    @property
    def enrollment_cls(self):
        return django_apps.get_model(self.enrollment_model)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollments = self.enrollment_cls.objects.all()
        subject_screening = self.subject_screening_cls.objects.all()
        subject_consent = self.subject_consent_cls.objects.all()

        enrolled_subjects = enrollments.count()
        screened_subjects = subject_screening.count()
        consented_subjects = subject_consent.count()

        context.update(

            consented_subjects=consented_subjects,
            enrolled_subjects=enrolled_subjects,
            screened_subjects=screened_subjects)

        return context
