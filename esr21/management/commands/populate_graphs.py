from django.core.management.base import BaseCommand
from esr21_reports.views.graphs_mixins import (AgeDistributionGraphMixin,
                                               ScreeningGraphMixin,
                                               EnrollmentGraphMixin)
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

    def populate_age_graph(self):
        age_distribution = AgeDistributionGraphMixin()
        for site in self.siteHelper.sites_names:
            age_dist = age_distribution.get_distribution_site(site)
            AgeStatistics.objects.update_or_create(
                site=site,
                min=age_dist[0],
                lowerquartile=age_dist[1],
                median=age_dist[2],
                upperquartile=age_dist[3],
                max=age_dist[4],
            )

    def populate_other_graphs(self):
        pass

    def populate_screening_data(self):
        screening = ScreeningGraphMixin()
        for site in self.siteHelper.sites_names:
            results = screening.get_screened_by_site(site_name_postfix=site)
            ScreeningStatistics.objects.update_or_create(
                site=site,
                passed=results[0],
                failed=results[1]
            )

    def populate_enrollement_data(self):
        enrollment = EnrollmentGraphMixin()
        for site in self.siteHelper.sites_names:
            male, female = enrollment.get_vaccinated_by_site(site)
            total = male + female
            EnrollmentStatistics.objects.update_or_create(
                site=site,
                total=total,
                male=male,
                female=female
            )
