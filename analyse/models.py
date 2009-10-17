from django.db import connection, models,settings
import string
from elementtree import ElementTree
from datetime import datetime
import os
from analyse.openFlashChart import Chart
import re


class Build(models.Model):
    number = models.TextField()
    name = models.TextField()
    scm_type = models.TextField()
    scm_revision = models.TextField()
    start_time = models.DateTimeField('build start')
    build_time = models.IntegerField('How long does this build take', default=0)
    is_passed = models.BooleanField('Does the build pass', default=False)
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
                build.is_passed = target.attrib["value"].find('Lbuild') > -1
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
    def passed_count(name):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where name = %s and is_passed = 1", [name])
        rate = cursor.fetchone()
        return rate[0]

    @staticmethod
    def total(name):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where name = %s", [name])
        total = cursor.fetchone()
        return total[0]

    @staticmethod
    def analyse(name):
        return Statistics(name = name, total = Build.total(name), passed = Build.passed_count(name))

class Statistics :

    def __init__(self, name=None, total = 0, passed = 0):
        self.name = name
        self.total = total
        self.passed = passed

    def generate_chart(self, forced=False):
        total_json_dir = os.path.join(settings.RESULT_ROOT, self.name)
        total_json_file = os.path.join(total_json_dir, 'total.txt');

        if not(os.path.exists(total_json_file)) or forced :
            chart = Chart()

            element1 = Chart()
            element1.values =  [self.passed, self.total - self.passed]
            element1.type = "pie"
            element1.alpha = 0.6
            element1.angle = 35
            element1.tip = '#val# of #total#<br>#percent# of 100%';
            element1.colours = ['#1C9E05','#FF368D']

            chart.elements = [element1]

            if not(os.path.exists(total_json_dir)):
                os.makedirs(total_json_dir)

            f = open(total_json_file, 'w')
            try:
                f.write(chart.create())
            finally:
                f.close()

class ThreeWeeksStatistics :
    def __init__(self, name=None, total = 0, passed = 0):
        self.name = name
        self.total = total
        self.passed = passed

    def generate_chart(self):
        chart = Chart()

        element1 = Chart()
        element1.values =  [self.passed, self.total - self.passed]
        element1.type = "pie"
        element1.alpha = 0.6
        element1.angle = 35
        element1.tip = '#val# of #total#<br>#percent# of 100%';
        element1.colours = ['#1C9E05','#FF368D']

        chart.elements = [element1]

        f = open("/Users/twer/Workspace/ianalyse/results/area-2.txt", 'w')
        try:
            f.write(chart.create())
        finally:
            f.close()

class BuildFactory :

    @staticmethod
    def create_builds (name = "", pattern = None):
        if pattern == None :
            pattern = "log.*.xml"

        builds = list();

        root = os.path.join(settings.CCLOGS, name);

        for eachfile in os.listdir(root):
            if None != re.match(pattern, eachfile) :
                build = Build.from_file(os.path.join (root, eachfile))
                build.save()
                builds.append(build)
        return builds;

        