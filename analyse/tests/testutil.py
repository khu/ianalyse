from analyse.config import Config
from django.db import settings

class TestUtils:
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