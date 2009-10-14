from django.db import models
import string
from elementtree import ElementTree 
from datetime import datetime


class Build(models.Model):
    number = models.TextField()
    name = models.TextField()
    scm_type = models.TextField()
    scm_revision = models.TextField()
    start_time = models.DateTimeField('build start')
    build_time = models.IntegerField('How long does this build take')
    passed = models.BooleanField('Does the build pass')
    last_pass = models.DateTimeField('When is the last successful date')

    def __unicode__(self):
        return self.name

    @staticmethod
    def from_xml(input):
        if isinstance(input, str) :
           build = Build()
           tree = ElementTree.fromstring(input)
           for target in tree.findall(".//property"):
               if (target.attrib['name'] == 'label'):
                   build.number = target.attrib["value"];
               elif (target.attrib['name'] == 'projectname'):
                   build.name = target.attrib["value"];
               elif (target.attrib['name'] == 'cctimestamp'):
                   build.start_time = datetime.strptime(target.attrib["value"], "%Y%m%d%H%M%S")
               elif (target.attrib['name'] == 'logfile'):
                   build.passed = target.attrib["value"].find('Lbuild') > -1
               elif (target.attrib['name'] == 'lastsuccessfulbuild'):
                   build.last_pass = datetime.strptime(target.attrib["value"], "%Y%m%d%H%M%S")

           return build      
        else:
            print 'here'
            b = Build()
            b.number = 1
            return b


