from django.test import TestCase
from analyse.models import Build, Builds, TopNStatistics, Builds
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases
import	cjson

class SuccessfulRateChartTests(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testGenerateTotalPassRate(self):
        builds = Builds.create_builds('connectfour4', SuccessfulRateChartTests.PATTERN);
        
        ndaysStat = TopNStatistics('connectfour4', builds)
        json_str = ndaysStat.successful_rate()
        json_obj = cjson.decode(json_str)


        self.assertEqual(2, len(json_obj['elements'][0]['values']));


