from django.test import TestCase
from analyse.models import Build, BuildFactory, OverallStatistics
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases
import shutil

class StatisticsGenerationTests(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.project_name = "myproject"
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'
        settings.RESULT_ROOT = os.path.join(settings.PROJECT_DIR, "tmp")
        os.makedirs_p(settings.RESULT_ROOT)

    def tearDown(self):
        os.rmdir_p(settings.RESULT_ROOT)

    def get_chart(self):
        return os.path.join(settings.RESULT_ROOT, self.project_name, 'pass_rate.txt')

    def testshouldGenerateChartIfThereIsNothing(self):
        statistics = OverallStatistics(self.project_name, 10, 3)
        statistics.generate_pass_rate();
        self.assertEquals(True, os.path.exists(self.get_chart()))

#    def testshouldNotGenerateChartIfTheChartIsGenerated(self):
#        statistics = OverallStatistics(self.project_name, 10, 3)
#
#        os.makedirs_p(os.path.join(settings.RESULT_ROOT, self.project_name))
#
#        chart = self.get_chart()
#        os.touch(chart)
#
#        statistics.generate_pass_rate();
#
#        content = open(chart, 'r').read()
#
#        self.assertEquals('', content)
#
#    def testshouldWhenUserExplictlyRequestForGeneration(self):
#        statistics = OverallStatistics(self.project_name, 10, 3)
#
#        os.makedirs_p(os.path.join(settings.RESULT_ROOT, self.project_name))
#
#        chart = self.get_chart()
#        os.touch(chart)
#
#        statistics.generate_pass_rate(True);
#
#        content = open(chart, 'r').read()
#
#        self.assertNotEquals("", content)
