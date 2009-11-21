from django.db import connection, models,settings
import string
from elementtree import ElementTree
from datetime import datetime
import os
import util.datetimeutils
from analyse.openFlashChart import Chart
import re
import util.datetimeutils
import analyse.ordered_dic
from analyse.config import Config, Configs

from xml.sax.handler import ContentHandler
from xml.sax import parse, parseString
import sys
from analyse.saxhandlers import *
from lxml import etree
import StringIO
import csv

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
        return self.name + " << " + str(self.is_passed) + " << " + str(self.start_time) + "\n"

    def day_of_start(self):
        return util.datetimeutils.begining_of_the_day(self.start_time)

    @staticmethod
    def from_xml(input):
        build = Build()
        parseString(input, MultipleHandlers(build))
        return build

    @staticmethod
    def from_file(input):
        build = Build()
        parse(input, MultipleHandlers(build))
        return build

    @staticmethod
    def select_values(file):
        tree = etree.parse(file)
        root = tree.getroot()
        result = []
        configs = Configs()
        config = configs.find('dummy')
        for setting in config.csv_settings() :
            try:
                select_xpath = etree.XPath(setting[1])
                result.append(select_xpath(root)[0])
            except Exception, e:
                result.append(None)
        return result

    @staticmethod
    def passed_count(name):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where name = %s and is_passed = 1", [name])
        rate = cursor.fetchone()
        return rate[0]

    @staticmethod
    def total_count(name):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where name = %s", [name])
        rate = cursor.fetchone()
        return rate[0]

    @staticmethod
    def pass_rate(name):
        cursor = connection.cursor()
        cursor.execute(
                "select (select CAST(count(1) AS REAL) from analyse_build where name = %s and is_passed = 1) / (select count(1) from analyse_build where name = %s)"
                ,
                [name, name])
        rate = cursor.fetchone()
        if rate[0] == None:
        	return 0.0
	else:
		return rate[0]


    @staticmethod
    def avg_build_time(name):
        cursor = connection.cursor()
        cursor.execute("select avg(build_time) from analyse_build where name = %s", [name])
        return  cursor.fetchone()[0]

    @staticmethod
    def started_build_at(name):
        cursor = connection.cursor()
        cursor.execute("select min(start_time) from analyse_build where name = %s", [name])
        return  cursor.fetchone()[0]

    @staticmethod
    def last_built_at(name):
        cursor = connection.cursor()
        cursor.execute("select max(start_time) from analyse_build where name = %s", [name])
        return  cursor.fetchone()[0]

    @staticmethod
    def total(name):
        cursor = connection.cursor()
        cursor.execute("select count(1) from analyse_build where name = %s", [name])
        total = cursor.fetchone()
        return total[0]

    @staticmethod
    def analyse_all(name, results):
        Build.view_all(name, results)
        stat = OverallStatistics(name = name, total = Build.total(name), passed = Build.passed_count(name))
        stat.generate_pass_rate()

        stat = TopNStatistics(name = name, builds = Build.objects.order_by('start_time'))
        stat.generate_successful_rate()
        stat.generate_build_times()
        stat.generate_per_build_time()

        return

    @staticmethod
    def view_all(name, results):
        results["total_count"] = Build.total_count(name)
        results["avg_time"] = Build.avg_build_time(name)             
        results["pass_rate"] = "%.2f%%" % (Build.pass_rate(name) * 100)
        results["started_build_at"] = Build.started_build_at(name)
        results["last_built_at"] = Build.last_built_at(name)
        return

class OverallStatistics :

    def __init__(self, name=None, total = 0, passed = 0):
        self.name = name
        self.total = total
        self.passed = passed

    def pass_rate(self):
        chart = Chart()

        element1 = Chart()
        element1.values =  [self.passed, self.total - self.passed]
        element1.type = "pie"
        element1.alpha = 0.6
        element1.angle = 35
        element1.tip = '#val# of #total#<br>#percent# of 100%';
        element1.colours = ['#1C9E05','#FF368D']

        chart.elements = [element1]
        return chart.create()

    def __getattr__(self, name):
        if not name.startswith("generate_"):
            raise AttributeError(name)
        field = name[len("generate_"):]
        result = getattr(self, field)()
        project_root = Config().result_dir(self.name)
        os.makedirs_p(project_root)
        total_json_file = os.path.join(project_root, field + '.txt');
        os.write_to_file(total_json_file, result)
        return lambda : {}

class TopNStatistics :
    def __init__(self, name=None, builds = list()):
        self.name = name
        self.builds = builds

    def per_build_time(self):
        builds = Builds()
        builds.builds = self.builds

        chart = Chart()

        values, labels, max_time = builds.per_build_time();
        element = Chart()
        element.type = "bar_glass"
        element.values = values
        

        chart.elements = [element]
        chart.y_axis = { "min": 0, "max": max_time + 10, "steps": 50}
        chart.x_axis = {"labels" : {"labels" : labels, "visible-steps": 2, "rotate": 90}}
        return chart.create()

    def successful_rate(self):
        chart = Chart()

        element = Chart()
        element.type = "line"
        element.dot_style = { "type": "dot" }
        element.width = 2
        element.colour = "#C4B86A"
        element.fill = "#1C9E05"
        element.fill_alpha = 0.7

        builds = Builds()
        builds.builds = self.builds
        values, min_date, max_date = builds.pass_rate_by_day()

        element.values = values
        chart.elements = [element]
        all_percentage = []

        for i in range(110):
            all_percentage.append(str(i) + "%");

        chart.y_axis   = { "min": 0, "max": 110, "steps": 10,  "labels" : {"labels" : all_percentage, "steps" : 20}}
        chart.x_axis   = { "min": min_date, "max": max_date, "steps": 86400,
                           "labels": { "text": "#date:l jS, M Y#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Pass rate over time."}
        return chart.create()

    def build_times(self):
        chart = Chart()

        element = Chart()
        element.type = "line"
        element.dot_style = { "type": "dot" }
        element.width = 2
        element.colour = "#0000ff"
        element.fill = "#1C9E05"
        element.fill_alpha = 0.7

        builds = Builds()
        builds.builds = self.builds
        
        values, min_date, max_date, max_time = builds.build_times()

        element.values = values
        chart.elements = [element]
        all_percentage = []

        chart.y_axis   = { "min": 0, "max": max_time + 10, "steps": 50,  "labels" : {"steps" : 20}}
        chart.x_axis   = { "min": min_date, "max": max_date, "steps": 86400,
                           "labels": { "text": "#date:l jS, M Y#", "steps": 86400, "visible-steps": 2, "rotate": 90 }}
        chart.title    = { "text": "Build time over time."}
        return chart.create()

    def __getattr__(self, name):
        if not name.startswith("generate_"):
            raise AttributeError(name)
        field = name[len("generate_"):]
        result = getattr(self, field)()
        
        total_json_file = os.path.join(Config().result_dir(self.name), field + '.txt');
        
        os.write_to_file(total_json_file, result)
        return lambda : {}

class Builds:
    def __init__(self):
        self.builds = []

    def group_by_each_day(self):
        grouped_builds = analyse.ordered_dic.ordered_dict()

        for build in self.builds :
            day_of_start = build.day_of_start()
            if (day_of_start not in grouped_builds):
                newbuilds = Builds()
                newbuilds.builds.append(build)
                grouped_builds[day_of_start] = newbuilds
            else :
                grouped_builds[day_of_start].builds.append(build)

        return grouped_builds

    def to_unix_timestamp(self, day_of_start):
        epoch = int(day_of_start.strftime('%s'))
        usec = day_of_start.microsecond
        return epoch + (usec / 1000000.0)

    def pass_rate_by_day(self) :
        arry = []
        builds = Builds()
        builds.builds = self.builds
        grped_builds = builds.group_by_each_day();
        min_date = None;
        max_date = None;

        for day_of_start in grped_builds.order() :
            timestamp = int(self.to_unix_timestamp(day_of_start));
            pass_rate = grped_builds[day_of_start].pass_rate()
            arry.append({"x" : timestamp, "y" : pass_rate * 100})
            if min_date == None or timestamp < min_date:
                min_date = timestamp;

            if max_date == None or timestamp >  max_date:
                max_date = timestamp;

        return arry,min_date, max_date

    def build_times(self):
        arry = []
        min_date = None;
        max_date = None;
        max_time = None
        for build in self.builds :
            timestamp = int(self.to_unix_timestamp(build.start_time));
            arry.append({"x" : timestamp, "y" : build.build_time})
            if min_date == None or timestamp < min_date:
                min_date = timestamp;

            if max_date == None or timestamp >  max_date:
                max_date = timestamp;

            if max_time == None or build.build_time > max_time:
                max_time = build.build_time

        return arry,min_date, max_date, max_time    

    def per_build_time(self):
        arry = []
        labels = []
        max_time = None
        for build in self.builds :
            timestamp = int(self.to_unix_timestamp(build.start_time));
            color = None;
            if build.is_passed:
                color = '#1C9E05'
            else:
                color = '#FF368D'                           

            arry.append({"top" : build.build_time, "colour": color})
            labels.append(str(build.start_time))
            if max_time == None or build.build_time > max_time:
                max_time = build.build_time
        return arry, labels, max_time

    def pass_count(self) :
        count = 0
        for build in self.builds :
            if build.is_passed :
                count = count + 1
        return count

    def pass_rate(self) :
        if len(self.builds) == 0:
            return 0

        return self.pass_count() / len(self.builds)
        
    def __unicode__(self):
        return "<Builds " + str(self.builds) + ">\n"


    @staticmethod
    def create_builds(config, pattern, required_builds):
        if pattern == None :
            pattern = "log.*.xml"

        Build.objects.all().delete()
           
        builds = list();
                 
        for eachfile in Builds.filter(config.logdir(), required_builds):
            if None != re.match(pattern, eachfile) :
                try :
                    build = Build.from_file(config.logfile(eachfile))
                    build.save()
                    builds.append(build)
                except Exception, e :
                    pass

        return builds;

    @staticmethod  
    def select_values_from(config, pattern, required_builds):
        if pattern == None :
            pattern = "log.*.xml"

        values = []
        for eachfile in Builds.filter(config.logdir(), required_builds):
            if None != re.match(pattern, eachfile) :
                try :
                    value = Build.select_values(config.logfile(eachfile))
                    values.append(value)
                except Exception, e :
                    pass
        return values
        
    @staticmethod
    def filter(root, required_builds): 
          files = os.sort_by_rule(root,"log([0-9]*).*.xml", 'asc')
          len_of_files = len(files)

          if required_builds < len_of_files :                 
              for i in range(0, len_of_files - required_builds) :
                  files.pop(0)

          return files

    @staticmethod
    def create_csv(name):
        config = Configs().find('dummy')
        arrays = Builds.select_values_from(config, None, config.builds())
        folder = Config().result_dir(name)
        writer = csv.writer(open(os.path.join(folder, name + '.csv'), 'w'), delimiter=',')
        writer.writerows(arrays)




