from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Config, Configs


class ConfigTests(TestCase):   
    original = os.environ["CONFIGS_DIR"]
    
    def setUp(self):
        self.config = Config(os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/ianalyse.cfg')))
        
    def tearDown(self):
         project1 = self.config.result_dir()
         if os.path.exists(project1) :
            os.rmdir_p(project1)
         os.environ["CONFIGS_DIR"] = ConfigTests.original
         
    def testShouldReturnTheAbsolutePathOfTheDefaultConfigFile(self):
        expected = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'configs'))
        os.environ.pop("CONFIGS_DIR")
        config = Configs()
        self.assertEquals(expected, config.abspath())

    def testShouldReturnSpecificConfigFile(self):
        expected = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))
        config = Configs(expected)
        self.assertEquals(expected, config.abspath())
    
    def testShouldReturnFalseWhenConfigFileIsMissing(self):
        not_exist_file = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/not.exist.cfg'))
        self.assertEquals(False, Config(not_exist_file).exist())
	  
    def testShouldReadTheLogDir(self):
        self.assertEquals('/var/logs', self.config.logdir())
	
    def testShouldReturnNDaysIfDefined(self):
        self.assertEquals(3, self.config.builds())
	
    def testShouldReturn14DaysAsDefaultValue(self):
        self.config = Config(os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/no_days.cfg')))
        self.assertEquals(30, self.config.builds())
	
    def testShouldAggregateTheColumnNamesAndXpathsAsDic(self):
        self.assertEquals('start time', self.config.csv_settings()[0][0])
        self.assertEquals('//property[@name=\'start time\']/@value', self.config.csv_settings()[0][1])
        self.assertEquals('buid time', self.config.csv_settings()[1][0])
        self.assertEquals('//build/@time', self.config.csv_settings()[1][1])

    def testShouldAggregateTheColumnNamesAndXpathsAsDic(self):
        self.assertEquals('start time', self.config.csv_keys()[0])
        self.assertEquals('buid time', self.config.csv_keys()[1])

    def testShouldReturnTrueIfAllResultsJsonGenerated(self):
        project1 = self.config.result_dir()
				
        os.touch(os.path.join(project1, 'build_times.txt'))
        os.touch(os.path.join(project1, 'pass_rate.txt'))
        os.touch(os.path.join(project1, 'per_build_time.txt'))
        os.touch(os.path.join(project1, 'successful_rate.txt'))
        
        self.assertEquals(True, self.config.has_result())


    def testShouldReturnFalseIfAnyResultJsonIsMissing(self):
        project1 = self.config.result_dir()
        os.makedirs_p(project1)
        os.touch(os.path.join(project1, 'pass_rate.txt'))
        self.assertEquals(False, self.config.has_result())        


    def testShouldReturnFalseIfAnyResultJsonGenerated(self):
        self.assertEquals(False, self.config.has_result())
        