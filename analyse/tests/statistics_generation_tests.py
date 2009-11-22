from django.test import TestCase
from analyse.models import Build, Builds, OverallStatistics
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases
import shutil
from analyse.config import Config

class StatisticsGenerationTests(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"
    original = Config.results_dir

    def temp_results_dir(self):
        return os.path.join(settings.PROJECT_DIR, "tmp")
        
    def setUp(self):
        self.project_name = "connectfour4"
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'
        self.results_root = os.path.join(settings.PROJECT_DIR, "tmp")

        os.makedirs_p(self.results_root)
        
        Config.results_dir = self.temp_results_dir

    def tearDown(self):
        Config.results_dir = StatisticsGenerationTests.original
        os.rmdir_p(self.results_root)

    def get_chart(self):
        return os.path.join(self.results_root, self.project_name, 'pass_rate.txt')

    def testshouldGenerateChartIfThereIsNothing(self):
        statistics = OverallStatistics(self.project_name, 10, 3)
        statistics.generate_pass_rate();
        self.assertEquals(True, os.path.exists(self.get_chart()))
