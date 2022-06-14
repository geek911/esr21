


from urllib.request import DataHandler
from django.core.management.base import BaseCommand
from esr21_reports.views.graphs_mixins import (AgeDistributionGraphMixin,
                                               ScreeningGraphMixin,
                                               EnrollmentGraphMixin,
                                               VaccinationGraphMixin)
from esr21_reports.models import (
    AgeStatistics, ScreeningStatistics, EnrollmentStatistics,
    VaccinationStatistics, DashboardStatistics)
from esr21_reports.views.enrollment_report_mixin import EnrollmentReportMixin
from esr21_reports.constants import (ENROLLED_STATISTICS, 
                                     VACCINATION_STATISTICS,
                                     DEMOGRAPHICS_STATISTICS,
                                     GENERAL_STATISTICS)


class Command(BaseCommand):

    help = 'Populate Dashboard Statistics'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DashboardStatistics.objects.all().delete()
        self.enrollment_mixin =  EnrollmentReportMixin()

    def handle(self, *args, **kwargs):
        self.populate_enrolled_statistics()
        
    def populate_enrolled_statistics(self):
        
        # setattr(enrollment_mixin, 'vaccination_model', 'esr21_subject.vaccinationdetails')
        
        
        for participants in self.enrollment_mixin.enrolled_participants:
            dashboard_stat = DashboardStatistics()
            dashboard_stat.type = ENROLLED_STATISTICS
            dashboard_stat.title = participants[0]
            dashboard_stat.gaborone = participants[1]
            dashboard_stat.maun = participants[2]
            dashboard_stat.serowe = participants[3]
            dashboard_stat.francistown = participants[4]
            dashboard_stat.selebi_phikwe = participants[5]
            dashboard_stat.save()
            
    def populate_vaccine_statistics(self):
        
        
        
            
        
    