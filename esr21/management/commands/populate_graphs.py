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
            site_id = self.siteHelper.get_site_id(site)
            min, lowerquartile, median, upperquartile, max, site_outliers = age_distribution.get_distribution_site(site_id)
            defaults = {
                'min': min,
                'lowerquartile': lowerquartile,
                'median': median,
                'upperquartile': upperquartile,
                'max': max,
                }
            AgeStatistics.objects.update_or_create(
                site=site,
                defaults=defaults
            )

    def populate_screening_data(self):
        screening = ScreeningGraphMixin()
        for site in self.siteHelper.sites_names:
            site_id = self.siteHelper.get_site_id(site)
            passed, failed = screening.get_screened_by_site(site_id=site_id)
            ScreeningStatistics.objects.update_or_create(
                site=site,
                defaults={
                    'passed': passed,
                    'failed': failed
                }
            )

    def populate_enrollement_data(self):
        enrollment = EnrollmentGraphMixin()
        for site in self.siteHelper.sites_names:
            site_id = self.siteHelper.get_site_id(site)
            male, female = enrollment.get_vaccinated_by_site(site_id)
            total = male + female
            defaults = {
                'total': total,
                'male': male,
                'female': female
            }
            EnrollmentStatistics.objects.update_or_create(
                site=site,
                defaults=defaults
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
            defaults = {
                'dose_1_percent': first_dose,
                'dose_2_percent': second_dose,
                'dose_3_percent': booster_dose,
                'overall_percent': vaccine.overal_site_dose_vaccination(
                    site_id=site_id)
            }

            VaccinationStatistics.objects.update_or_create(
                site=site,
                defaults=defaults
            )
