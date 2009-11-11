import os                                                  
from django.conf import settings
import ConfigParser

class Config:
    DEFAULT_FILES_TO_PROCESS = 30
    def __init__(self, config_file = None):
        config = config_file
        if None ==  config_file :
            config = os.environ.get("CONFIG_FILE")

        if None == config :
            config = os.path.join(settings.PROJECT_DIR, 'ianalyse.cfg')

        self.config_file = config
    
    def abspath(self):
        return os.path.abspath(self.config_file)                                        
    
    def exist(self):
        return os.path.exists(self.abspath())
    
    def logdir(self): 
        def anonymous(config): return config.get('Basic', 'logdir', 0)
        return self.__readattr__(anonymous)
    
    def builds(self):
        def anonymous(config): 
            try:                                        
                return config.getint('Basic', 'builds')
            except Exception, e:
                return Config.DEFAULT_FILES_TO_PROCESS
        return self.__readattr__(anonymous)
        
    def csv_settings(self):
        def anonymous(config): return config.items("CSV")
        return self.__readattr__(anonymous) 

    def view_all(self, results):
        results['config_file'] = self.abspath()

    def __readattr__(self, func):
       config = ConfigParser.ConfigParser()
       config.read(self.abspath())
       return func(config)
        
