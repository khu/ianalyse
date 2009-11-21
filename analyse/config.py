import os                                                  
from django.conf import settings
import ConfigParser

class Configs:
    def __init__(self, config_dir = None):
        configs = config_dir
        if None ==  configs :            
            configs = os.environ.get("CONFIGS_DIR")

        if None == configs :
            configs = os.path.join(settings.PROJECT_DIR, 'configs')

        self.configs = configs

    def abspath(self):
        return os.path.abspath(self.configs)                                        

    def find(self, id):
        return Config(os.path.join(self.configs, 'ianalyse.cfg'))
    
    def __str__( self ):
            return 'the configs dir location is [' + self.configs + ']'
    
class Config:
    DEFAULT_FILES_TO_PROCESS = 30
    def __init__(self, config_file = None):
        self.config_file = config_file
    
    def project_name(self):
        def anonymous(config): return config.get('Basic', 'name', 0)
        return self.__readattr__(anonymous)
            
    def abspath(self):
        return os.path.abspath(self.config_file)                                        
    
    def exist(self):
        return os.path.exists(self.abspath())
    
    def logdir(self): 
        def anonymous(config): return config.get('Basic', 'logdir', 0)
        return self.__readattr__(anonymous)
    
    def logfile(self, name):
        return os.path.join(self.logdir(), name)
    
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

    def results_dir(self):
        return os.path.join(settings.PROJECT_DIR, 'results')

    def result_dir(self, name):
       return os.path.join(self.results_dir(), name)

    def has_result(self, name):
        if not os.path.exists(self.result_dir(name)) :
             return False

        total_generated_json_files = 4        
        return len(os.listdir(self.result_dir(name))) >= total_generated_json_files

    def __readattr__(self, func):
       config = ConfigParser.ConfigParser()
       config.read(self.abspath())
       return func(config)
       
    def __str__( self ):
        return 'the config file location is [' + self.config_file + ']'
        
        
        
