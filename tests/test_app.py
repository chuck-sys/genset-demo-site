import os
from app import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Properly configure the site
        app.config.from_object('test_config')

        self.app = app.test_client()

    def tearDown(self):
        pass
    
    def _static_getter(self, path, text):
        res = self.app.get(path)
        return text in res.data
    
    def test_root(self):
        assert self._static_getter('/', b'About the Project')

    def test_about(self):
        assert self._static_getter('/about', b'About the Project')
        
    def test_get_upload(self):
        assert self._static_getter('/upload', b'405')
        
    def test_not_founds(self):
        assert self._static_getter('/blahblahb', b'404')