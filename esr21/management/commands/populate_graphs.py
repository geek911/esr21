import json
from django.core.management.base import BaseCommand
from esr21_reports.views.graphs_mixins import (AgeDistributionGraphMixin,
                                               ScreeningGraphMixin,
                                               EnrollmentGraphMixin,
                                               VaccinationGraphMixin)
from esr21_reports.models import (
    AgeStatistics, ScreeningStatistics, EnrollmentStatistics,
    VaccinationStatistics, DashboardStatistics)
from esr21_reports.views.enrollment_report_mixin import EnrollmentReportMixin
from esr21_reports.views.psrt_mixins import DemographicsMixin
from esr21_reports.views.adverse_events import AdverseEventRecordViewMixin, SeriousAdverseEventRecordViewMixin

from esr21_reports.views.site_helper_mixin import SiteHelperMixin


class Command(BaseCommand):

    help = 'Populate reports forms'
    siteHelper = SiteHelperMixin()

    def handle(self, *args, **kwargs):
        self.populate_age_graph()
        self.populate_screening_data()
        self.populate_enrollement_data()
        self.populate_vaccination_data()
        self.populate_enrollement_enrollement_with_conhorts()
        self.populate_vaccinate()
        self.populate_demographics()
        self.populate_genaral_statistics()

    def populate_age_graph(self):
        age_distribution = AgeDistributionGraphMixin()
        for site in self.siteHelper.sites_names:
            min, lowerquartile, median, upperquartile, max = age_distribution.get_distribution_site(site)
            AgeStatistics.objects.update_or_create(
                site=site,
                min=min,
                lowerquartile=lowerquartile,
                median=median,
                upperquartile=upperquartile,
                max=max,
            )

    def populate_other_graphs(self):
        pass

    def populate_screening_data(self):
        screening = ScreeningGraphMixin()
        for site in self.siteHelper.sites_names:
            site_id = self.siteHelper.get_site_id(site)
            passed, failed = screening.get_screened_by_site(site_id=site_id)
            ScreeningStatistics.objects.update_or_create(
                site=site,
                passed=passed,
                failed=failed
            )

    def populate_enrollement_data(self):
        enrollment = EnrollmentGraphMixin()
        for site in self.siteHelper.sites_names:
            site_id = self.siteHelper.get_site_id(site)
            male, female = enrollment.get_vaccinated_by_site(site_id)
            total = male + female
            EnrollmentStatistics.objects.update_or_create(
                site=site,
                total=total,
                male=male,
                female=female
            )
            
    def populate_enrollement_enrollement_with_conhorts(self):
        enrollment = EnrollmentReportMixin()
        enrolled_participants = enrollment.enrolled_participants
        enrolled_participants_json = json.dumps(enrolled_participants)
        
        DashboardStatistics.objects.update_or_create(
            key = 'enrolled_statistics',
            value = enrolled_participants_json
        )
        
    def populate_vaccinate(self):
        enrollment = EnrollmentReportMixin()
        
        vaccinated_participants = [
                enrollment.received_one_doses,
                enrollment.received_two_doses,
                enrollment.received_booster_doses,
        ]
        
        vaccinated_participants_json = json.dumps(vaccinated_participants)
        
        DashboardStatistics.objects.update_or_create(
            key = 'vaccinated_statistics',
            value = vaccinated_participants_json
        )
        
    def populate_demographics(self):
        demographics = DemographicsMixin()
        demographics_json = json.dumps(demographics.demographics_statistics)
        
        DashboardStatistics.objects.update_or_create(
            key = 'demographics_statistics',
            value = demographics_json
        )
        
    def populate_genaral_statistics(self):
        ae = AdverseEventRecordViewMixin()
        sae = SeriousAdverseEventRecordViewMixin()
        
        ae_json = json.dumps(ae.ae_statistics)
        sae_json = json.dumps(sae.sae_statistics)
        
        DashboardStatistics.objects.update_or_create(
            key='ae_statistics', 
            value=ae_json
        )
        
        DashboardStatistics.objects.update_or_create(
            key='sae_statistics', 
            value=sae_json
        )
            
            
    def populate_vaccination_data(self):
        vaccine = VaccinationGraphMixin()
        for site in self.siteHelper.sites_names:
            site_id = self.siteHelper.get_site_id(site)
            first_dose = vaccine.site_dose_vaccination(
                site_id=site_id, dose='first_dose')
            second_dose = vaccine.site_dose_vaccination(
                site_id=site_id, dose='second_dose')
            booster_dose = vaccine.site_dose_vaccination(
                site_id=site_id, dose='booster_dose')
            VaccinationStatistics.objects.update_or_create(
                site=site,
                dose_1_percent=first_dose,
                dose_2_percent=second_dose,
                dose_3_percent=booster_dose
            )
        
