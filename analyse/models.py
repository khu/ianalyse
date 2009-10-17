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

    @staticmethod
    def analyse_x(name):
        return ThreeWeeksStatistics(name = name, builds = list())

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

            os.makedirs_p(total_json_dir)
            os.write_to_file(total_json_file, chart.create())

class ThreeWeeksStatistics :
    def __init__(self, name=None, builds = list()):
        self.name = name
        self.builds = builds

    '''
    { "elements": [ { "type": "area", "width": 2, "dot-style": { "type": "hollow-dot" }, "colour": "#838A96", "fill": "#E01B49", "fill-alpha": 0.4, "values": [{ "x": 1230768000, "y": 10.3677462 }, { "x": 1230854400, "y": 27.32435671 }, { "x": 1230940800, "y": 35.28000201 }] } ], "title": { "text": "Area Chart" }, "y_axis": { "stroke": 3, "colour": "#D7E4A3", "tick-length": 7, "grid-colour": "#A2ACBA", "min": 0, "max": 110, "steps": 20, "labels": { "labels": [
        ], "steps": 20 } } , } }
    '''
    def successful_rate(self):
        chart = Chart()
        stra = []
        for i in range(110):
            stra.append(str(i) + "%");

        element = Chart()
        element.type = "area"
        element.dot_style = { "type": "hollow-dot" }
        element.width = 2
        element.colour = "#C4B86A"
        element.fill = "#1C9E05"
        element.fill_alpha = 0.7
        element.values = [{ "x": 1230768000, "y": 12.103677462 }, { "x": 1230854400, "y": 12.2732435671 }, { "x": 1230940800, "y": 10.3528000201 }, { "x": 1231027200, "y": 8.10799376173 }]
        #"stroke": 3, "colour": "#D7E4A3", "tick-length": 7, "grid-colour": "#A2ACBA", "min": 0, "max": 110, "steps": 20, "labels":

        #"x_axis": { "min": 1230768000, "max": 1230940800, "steps": 86400, "labels": { "text": "#date:l jS, M Y#", "steps": 86400, "visible-steps": 2, "rotate": 90 }
        chart.elements = [element]
        chart.y_axis   = { "min": 0, "max": 110, "steps": 10,  "labels" : {"labels" : stra, "steps" : 20}}
        chart.x_axis   = { "min": 1230768000, "max": 1230940800, "steps": 86400, "labels": { "text": "#date:l jS, M Y#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Pass rate over time."}
        return chart.create()


    #"x_axis": { "min": 1230768000, "max": 1230940800, "steps": 86400, "labels": { "text": "#date:l jS, M Y#", "steps": 86400, "visible-steps": 2, "rotate": 90 }
    def generate_successful_rate_chart(self):
        total_json_file = os.path.join(os.path.join(settings.RESULT_ROOT, self.name), 'successful_rate.txt');

        print self.successful_rate()
        a = '''
        { "elements": [ { "type": "area", "width": 2, "dot-style": { "type": "hollow-dot" }, "colour": "#838A96", "fill": "#E01B49", "fill-alpha": 0.4,
            "values": [ 0, 0.377471728511, 0.739894850386, 1.07282069945, 1.36297657271, 1.59879487114, 1.77087426334, 1.87235448698, 1.89918984578, 1.85031049867, 1.72766511097, 1.53614316726, 1.28338004305, 0.979452606461, 0.636477485296, 0.268128015314, -0.110910872512, -0.485528093851, -0.84078884226, -1.16252999279, -1.43792474109, -1.65599396759, -1.80804394039, -1.8880129069, -1.89271275679, -1.82195612186, -1.67856384587, -1.46825252636, -1.19940661196, -0.882744140886, -0.530889446578 ] } ],
            "title": { "text": "Area Chart" },
            "y_axis": { "min": -20, "max": 20, "steps": 2, "labels": {"labels" : ["a", "b", "c", "d", "e", "f"], "steps" : 2}, "offset": 0 }, "
             x_axis": { "labels": { "steps": 4, "rotate": 270 }, "steps": 2 } }
        '''
        os.write_to_file(total_json_file, self.successful_rate())

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

        