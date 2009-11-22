from analyse.config import Config
from django.db import settings
import os
import util.osutils

class TestUtils:
        
    def connectfour(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/connectfour4'

    def cclive_release_jdk(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'        
     
    def csv_settings(self):
        return [('project name', '//property[@name="projectname"]/@value'),
            ("label", '//property[@name="label"]/@value'),
            ('buid time', '//build/@time'),
            ('something wrong', '//not right')
            ]
        
    def connectfour_config(self):
        config = Config(settings.PROJECT_DIR + '/analyse/tests/fixtures/config/connectfour4.cfg')
        config.logdir = self.connectfour
        config.csv_settings = self.csv_settings 
        return config
    
    def cclive_config(self):
        config = Config(settings.PROJECT_DIR + '/analyse/tests/fixtures/config/cclive.cfg')
        config.logdir = self.cclive_release_jdk
        config.csv_settings = self.csv_settings
        return config
    
    def cleanup_results(self):
        results_dir = os.path.join(settings.PROJECT_DIR, 'results')
        if os.path.exists(results_dir) :
            os.rmdir_p(results_dir) 

    def last_modified_on(self, pj):
        results = {}
        results_dir = os.path.join(settings.PROJECT_DIR, 'results')
        result_dir = os.path.join(results_dir, pj)
        for file in os.listdir(result_dir):
            results[file] = os.path.getmtime(os.path.join(result_dir, file))
        return results
        
    def cleantemp(self):
        temp_dir = os.path.join(settings.PROJECT_DIR, 'temp')
        if os.path.exists(temp_dir):
            os.rmdir_p(temp_dir)
    
    def write_to_temp(self, file, content):
        temp_dir = os.path.join(settings.PROJECT_DIR, 'temp')
        os.makedirs_p(temp_dir)
        temp_file = os.path.join(temp_dir, file)
        os.touch(temp_file)
        f = open(temp_file, 'w')
        f.write(content)
        return temp_file
        