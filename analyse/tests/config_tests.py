from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Config


class ConfigTests(TestCase):   
    def setUp(self):
        self.config_file = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'ianalyse.cfg'))

    def testShouldReturnTheAbsolutePathOfTheConfigFile(self):
	    config = Config()
	    self.assertEquals(self.config_file, config.abspath())
	                                              
    
    def testShouldThrowExceptionWhenConfigFileIsMissing(self):
        pass
	  
    def testShouldReadTheLogDir(self):
	    pass
	
    def testShouldReturnNDaysIfDefined(self):
	    pass
	
    def testShouldReturn14DaysAsDefaultValue(self):
	    pass
	
    def testShouldAggregateTheColumnNamesAndXpathsAsDic(self):
	    pass                                   
	
    def testShouldAlwaysReadFromTheFile(self):
	    pass
	
