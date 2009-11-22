from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Config, Configs
from analyse.tests.testutil import TestUtils

class ConfigsTests(TestCase):
    def setUp(self):
        self.configs_root = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))
        self.configs = Configs(self.configs_root)
        
    def tearDown(self):
        pass
        
    def testShouldReturnTheConfigFilesUnderConfigsRoot(self):
        self.assertEquals(len(os.listdir(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))), self.configs.size())
        self.assertEquals(os.path.join(self.configs_root, 'ianalyse.cfg'), self.configs['ianalyse'].config_file)
        self.assertEquals(os.path.join(self.configs_root, 'no_days.cfg'), self.configs['no_days'].config_file)
        
        
