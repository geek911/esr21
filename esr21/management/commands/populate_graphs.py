from django.core.management.base import BaseCommand
from esr21_reports.views.graphs_mixins import AgeDistributionGraphMixin
from esr21_reports.models import AgeStatistics


class Command(BaseCommand):

    help = 'Populate reports forms'

    def handle(self, *args, **kwargs):
        self.populate_age_graph()

    def populate_age_graph(self):
        age_distribution = AgeDistributionGraphMixin()
        for site in age_distribution.sites_names:
            age_dist = age_distribution.get_distribution_site(site)
            age_stats = AgeStatistics(
                site=site,
                min=age_dist[0],
                lowerquartile=age_dist[1],
                median=age_dist[2],
                upperquartile=age_dist[3],
                max=age_dist[4],
            )
            age_stats.save()

    def populate_other_graphs(self):
        pass
