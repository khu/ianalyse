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
        self.assertEquals(3, self.config.days())
	
    def testShouldReturn14DaysAsDefaultValue(self):
        self.config = Config(os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/no_days.cfg')))
        self.assertEquals(14, self.config.days())
	
    def testShouldAggregateTheColumnNamesAndXpathsAsDic(self):
        self.assertEquals('start time', self.config.csv_settings()[0][0])
        self.assertEquals('//property[@name=\'start time\']/@value', self.config.csv_settings()[0][1])
        self.assertEquals('buid time', self.config.csv_settings()[1][0])
        self.assertEquals('//build/@time', self.config.csv_settings()[1][1])


		
