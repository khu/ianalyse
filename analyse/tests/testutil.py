from analyse.config import Config
from django.db import settings
import os
import util.osutils

class TestUtils:

    def __init__(self):
        self.config = Config()
        
    def connectfour(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/connectfour4'

    def cclive_release_jdk(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'        
     
    def connectfour_config(self):
        config = Config()
        config.logdir = self.connectfour
        return config
    
    def cclive_config(self):
        config = Config()
        config.logdir = self.cclive_release_jdk
        return config
    
    def cleanup_results(self):
        results_dir = self.config.results_dir()
        if os.path.exists(results_dir) :
            os.rmdir_p(results_dir) 

    def last_modified_on(self, pj):
        results = {}
        result_dir = os.path.join(self.config.result_dir(pj))
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
        