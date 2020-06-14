from django.test import TestCase
from .file_handlers import VisaTDCsvFileHandler

class VisaTDCsvFileHandlerTests(TestCase):
    
    def setUp(self):
        self.sut = VisaTDCsvFileHandler()
    
    def test__success(self):
        pass
