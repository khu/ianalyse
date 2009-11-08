import os                                                  
from django.conf import settings

class Config:
    def __init__(self, config_file = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'ianalyse.cfg'))):
        self.config_file = config_file
    
    def abspath(self):
        return self.config_file
    