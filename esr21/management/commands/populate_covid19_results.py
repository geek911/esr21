from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand
from edc_base.utils import get_utcnow

from edc_senaite_interface.classes import AnalysisResult


class Command(BaseCommand):

    help = 'Populate covid 19 results form, (bhplims integration)'

    @property
    def subject_requisition_cls(self):
        return django_apps.get_model('esr21_subject.subjectrequisition')

    @property
    def covid19_results(self):
        return django_apps.get_model('esr21_subject.covid19results')

    @property
    def subject_visit(self):
        return django_apps.get_model('esr21_subject.subjectvisit')

    def handle(self, *args, **kwargs):
        analysis_result = AnalysisResult(host=settings.HOST)

        authenticated = analysis_result.auth(
            settings.SENAITE_USER, settings.SENAITE_PASS)

        requisition_idxs = self.subject_requisition_cls.objects.filter(
            panel__name='sars_cov2_pcr').values_list(
                'subject_visit__subject_identifier', 'subject_visit__visit_code')

        if authenticated:
            result = None
            for requisition_idx in requisition_idxs:
                result = analysis_result.get_results(
                    participant_id=requisition_idx[0],
                    visit_code=requisition_idx[1])
                print('>>>', result)

                if result:
                    try:
                        subject_visit = self.subject_visit.objects.get(
                            subject_identifier=requisition_idx[0],
                            visit_code=requisition_idx[1],)
                    except self.subject_visit.DoesNotExist:
                        pass
                    else:
                        created, _ = self.covid19_results.objects.update_or_create(
                            subject_visit=subject_visit,
                            covid_result=result)
