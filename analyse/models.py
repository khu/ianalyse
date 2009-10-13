from django.db import models
import string
import new

class Build(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    scm_type = models.TextField()
    scm_revision = models.TextField()
    start_time = models.DateTimeField('build start')
    build_time = models.IntegerField('How long does this build take')
    passed = models.BooleanField('Does the build pass')
    last_pass = models.TextField('When is the last successful date')

    def __unicode__(self):
        return self.name

    @staticmethod
    def from_xml(input):
        if isinstance(input, str) :
            return Build(number = 1)
        else:
            print 'here'
            b = Build()
            b.number = 1
            return b


