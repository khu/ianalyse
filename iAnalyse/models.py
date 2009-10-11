from django.db import models

# Create your models here.
from django.db import models

class Build(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    scm_type = models.TextField()
    scm_revision = models.TextField()
    start_time = models.DateTimeField('build start')
    build_time = models.IntegerField('How long does this build take')
    passed = models.BooleanField('Does the build pass')
    last_pass = models.TextField('When is the last successful date')
    

__unicode__(self):
   return self.name

