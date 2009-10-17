from django.test import TestCase
from analyse.models import Build
from analyse.models import BuildFactory
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases

class SuccessfulRateChartTests(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testGenerateTotalPassRate(self):
        BuildFactory.create_builds('connectfour4', SuccessfulRateChartTests.PATTERN);
        self.assertEqual(2, Build.total('connectfour4'));
        self.assertEqual(1, Build.passed_count('connectfour4'));

    def testGenerateTotalBuilds(self):
        BuildFactory.create_builds('connectfour4', SuccessfulRateChartTests.PATTERN);
        self.assertEqual(2, Build.total('connectfour4'));
