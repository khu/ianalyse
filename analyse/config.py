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
        self.config_dir = configs
        self.configs = {}
        for file in os.listdir(self.config_dir):
            names = os.path.splitext(file)
            if names[1] == '.cfg':
                id = names[0]
                self.configs[id] = Config(os.path.join(self.config_dir, file))

    def abspath(self):
        return os.path.abspath(self.config_dir)                                        

    def find(self, id):
        if id == None :
            return self.configs.items()[0][1]
        else :
            return self.configs[id]

    def is_empty(self):
        return len(self.configs) == 0

    def size(self):
        return len(self.configs)

    def results_dir(self):
        return os.path.join(settings.PROJECT_DIR, 'results')

    def items(self):
        return self.configs.items()

    def __iter__(self):
        return self.configs.__iter__()
    
    def __getitem__(self, index):
        return self.configs.__getitem__(index)

    def __str__( self ):
            return 'the configs dir location is [' + self.config_dir + ']'
    
class Config:
    DEFAULT_FILES_TO_PROCESS = 30
    def __init__(self, config_file):
        self.config_file = config_file
        self.id = os.path.splitext(os.path.split(config_file)[1])[0]
                
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
    
    def csv_keys(self):
        settings = self.csv_settings()
        array = []
        for setting in settings :
            array.append(setting[0])
        return array

    def results_dir(self):
        return os.path.join(settings.PROJECT_DIR, 'results')

    def result_dir(self):
       return os.path.join(self.results_dir(), self.id)

    def has_result(self):
        if not os.path.exists(self.result_dir()) :
             return False

        total_generated_json_files = 4        
        return len(os.listdir(self.result_dir())) >= total_generated_json_files

    def status(self):
        if self.has_result() :
            return 'OK'
        else :
            return 'MISSING REPORTS'

    def __readattr__(self, func):
       config = ConfigParser.ConfigParser()
       config.read(self.abspath())
       return func(config)

    def content(self):
       return open(self.config_file).read()

    def __str__( self ):
        return 'the config file location is [' + self.config_file + ']'
    
        
        
