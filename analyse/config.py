import os                                                  
from django.conf import settings
import ConfigParser

class Config:
    def __init__(self, config_file = os.path.join(settings.PROJECT_DIR, 'ianalyse.cfg')):
        self.config_file = config_file
    
    def abspath(self):
        return os.path.abspath(self.config_file)                                        
    
    def exist(self):
        return os.path.exists(self.abspath())
    
    def logdir(self): 
        config = ConfigParser.ConfigParser()
        config.read(self.abspath())
        return config.get('Basic', 'logdir', 0)
    