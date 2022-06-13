from django.core.management.base import BaseCommand
from esr21_reports.views.graphs_mixins import (AgeDistributionGraphMixin,
                                               ScreeningGraphMixin,
                                               EnrollmentGraphMixin,
                                               VaccinationGraphMixin)
from esr21_reports.models import (
    AgeStatistics, ScreeningStatistics, EnrollmentStatistics,
    VaccinationStatistics)
from esr21_reports.views.site_helper_mixin import SiteHelperMixin


class Command(BaseCommand):

    help = 'Populate reports forms'
    siteHelper = SiteHelperMixin()

    def handle(self, *args, **kwargs):
        self.populate_age_graph()
        self.populate_screening_data()
        self.populate_enrollement_data()
        self.populate_vaccination_data()

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

    def populate_vaccination_data(self):
        vaccine = VaccinationGraphMixin()
        for site in self.siteHelper.sites_names:
            site_id = self.siteHelper.get_site_id(site)
            first_dose = vaccine.site_dose_vaccination(
                site_id=site_id, dose='first_dose')
            second_dose = vaccine.site_dose_vaccination(
                site_id=site_id, dose='first_dose')
            booster_dose = vaccine.site_dose_vaccination(
                site_id=site_id, dose='first_dose')
            VaccinationStatistics.objects.update_or_create(
                site=site,
                dose_1=first_dose,
                dose_2=second_dose,
                dose_3=booster_dose
            )
        pass
