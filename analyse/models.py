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
            os.write_to_file(total_json_file, chart.create)

class ThreeWeeksStatistics :
    def __init__(self, name=None, builds = list()):
        self.name = name
        self.builds = builds

    def successful_rate(self):
        chart = Chart()

        element = Chart()
        element.type = "area"
        element.width = 2
        element.colour = "#C4B86A"
        element.fill = "#C4B86A"
        element.fill_alpha = 0.7
        element.on_show = { "type": "pop-up", "cascade": 2, "delay": 0.5 }
        element.values = [ 3, 3.37747172851, 3.73989485039, 4.07282069945, 4.36297657271, 4.59879487114, 4.77087426334,
                           4.87235448698, 4.89918984578, 4.85031049867, 4.72766511097, 4.53614316726, 4.28338004305,
                           3.97945260646, 3.6364774853, 3.26812801531, 2.88908912749, 2.51447190615, 2.15921115774,
                           1.83747000721, 1.56207525891, 1.34400603241, 1.19195605961, 1.1119870931, 1.10728724321,
                           1.17804387814, 1.32143615413, 1.53174747364, 1.80059338804, 2.11725585911, 2.46911055342,
                           2.84213013465, 3.22144348922, 3.59192859068, 3.93881536716, 4.24827453757, 4.50796894131,
                           4.70754538204, 4.83904737686, 4.89723235621, 4.87978066858, 4.78738805769, 4.62373792537,
                           4.39535448596, 4.11134266649, 3.78302512196, 3.42349083679, 3.04707330836, 2.66877911568,
                           2.30368965442, 1.96635988931, 1.67023809357, 1.42712970874, 1.24672669894, 1.13622116287,
                           1.10001860755, 1.13956231461, 1.25327580124, 1.43662566956, 1.68230233892, 1.9805114558,
                           2.31936436375, 2.68535206665, 3.06388378972, 3.43986866769, 3.79831736997, 4.12493967794,
                           4.40671419091, 4.63240744823, 4.79302177194, 4.88215397582, 4.89625064016, 4.83474977544,
                           4.70010322707, 4.49767892801, 4.2355468963, 3.92415750882, 3.57592487782, 3.20473193937,
                           2.82537698457, 2.45298369834, 2.10239822584, 1.78759730354, 1.52113105078, 1.3136226362,
                           1.17334476543, 1.10588987452, 1.11394717711, 1.19719545396, 1.35231585898, 1.57312423113,
                           1.85081763743, 2.17432531806, 2.5307500427, 2.90588228233, 3.28476669836, 3.65229836476,
                           3.9938249538, 4.29573087813, 4.54598010126, 4.73459597638, 4.85405898376, 4.89960651027,
                           4.86942271978, 4.76471094475, 4.58964571322, 4.35120632352, 4.05889860168, 3.72437593414,
                           3.36097468401, 2.98318251235 ]
        element.y_axis =  { "min": 0, "max": 8, "steps": 2, "labels": None, "offset": 0 }
        element.x_axis =  { "labels": { "steps": 4, "rotate": 270 }, "steps": 2 }

        chart.elements = [element]
        return chart.create()

    def generate_successful_rate_chart(self):
        total_json_file = os.path.join(os.path.join(settings.RESULT_ROOT, self.name), 'successful_rate.txt');

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

        