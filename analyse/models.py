from django.db import connection, models
import string
from elementtree import ElementTree
from datetime import datetime
import os

class Build(models.Model):
    number = models.TextField()
    name = models.TextField()
    scm_type = models.TextField()
    scm_revision = models.TextField()
    start_time = models.DateTimeField('build start')
    build_time = models.IntegerField('How long does this build take', default=0)
    passed = models.BooleanField('Does the build pass', default=False)
    last_pass = models.DateTimeField('When is the last successful date')

    def __unicode__(self):
        return self.name

    @staticmethod
    def parse_build(tree):
        build = Build()
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

    @staticmethod
    def from_xml(input):
        tree = ElementTree.fromstring(input)
        return Build.parse_build(tree);

    @staticmethod
    def from_file(input):
        tree = ElementTree.parse(input)
        return Build.parse_build(tree);

    @staticmethod
    def pass_rate(name):
        cursor = connection.cursor()
        cursor.execute(
                "select ((select CAST(count(1) AS REAL) from analyse_build where name = %s and passed = 1) / (select count(1) from analyse_build where name = %s))"
                , [name, name])
        rate = cursor.fetchone()
        return rate[0]

    @staticmethod
    def total(name):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where name = %s", [name])
        total = cursor.fetchone()
        return total[0]

class BuildFactory :
    @staticmethod
    def create_builds():
        builds = list();
        root = "/Users/twer/Workspace/ianalyse/analyse/tests/fixtures/connectfour4";
        for eachfile in os.listdir(root):
            builds.append(Build.from_file(os.path.join (root, eachfile)))
        for eachbuild in builds:
            eachbuild.save()
        return builds;
       
