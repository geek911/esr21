from django.core.management.base import BaseCommand

from esr21_export.views import ListBoardViewMixin
from esr21_export.identifiers import ExportIdentifier


class Command(BaseCommand):

    help = 'Export vaccine data'

    def add_arguments(self, parser):
        parser.add_argument(
            'export_type', type=str, help='Type of export to execute.')
        parser.add_argument(
            'email', type=str, help='Email to update after download is complete..')

    def handle(self, *args, **kwargs):
        export_type = kwargs.get('export_type')
        email = kwargs.get('email')
        if export_type == 'all_data':
            self.export_all_data(email=email)
        if export_type == 'subject_data':
            self.export_subject_data(email=email)
        elif export_type == 'non_crf_data':
            self.export_non_crf_data(email=email)
        elif export_type == 'metadata_data':
            self.export_metadata_data(email=email)

    def export_all_data(self, email=None):
        view_cls = ListBoardViewMixin(to_email=email)
        view_cls.identifier_cls = ExportIdentifier
        view_cls.download_all_data()

    def export_subject_data(self, email=None):
        view_cls = ListBoardViewMixin(to_email=email)
        view_cls.identifier_cls = ExportIdentifier
        view_cls.download_subject_data()

    def export_non_crf_data(self, email=None):
        view_cls = ListBoardViewMixin(to_email=email)
        view_cls.identifier_cls = ExportIdentifier
        view_cls.download_non_crf_data()

    def export_metadata_data(self, email=None):
        view_cls = ListBoardViewMixin(to_email=email)
        view_cls.identifier_cls = ExportIdentifier
        view_cls.download_medata()
