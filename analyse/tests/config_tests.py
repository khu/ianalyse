from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Config


class ConfigTests(TestCase):   
    def setUp(self):
        self.config = Config(os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/ianalyse.cfg')))
        
    def testShouldReturnTheAbsolutePathOfTheDefaultConfigFile(self):
        expected = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'ianalyse.cfg'))
        config = Config()
        self.assertEquals(expected, config.abspath())

    def testShouldReturnSpecificConfigFile(self):
        expected = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/ianalyse.cfg'))
        config = Config(expected)
        self.assertEquals(expected, config.abspath())
    
    def testShouldReturnFalseWhenConfigFileIsMissing(self):
        not_exist_file = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/not.exist.cfg'))
        self.assertEquals(False, Config(not_exist_file).exist())
	  
    def testShouldReadTheLogDir(self):
        self.assertEquals('/var/logs', self.config.logdir())
	
    def testShouldReturnNDaysIfDefined(self):
	    pass
	
    def testShouldReturn14DaysAsDefaultValue(self):
	    pass
	
    def testShouldAggregateTheColumnNamesAndXpathsAsDic(self):
	    pass                                   
	
    def testShouldAlwaysReadFromTheFile(self):
	    pass
	
