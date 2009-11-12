from django.test import TestCase
from analyse.models import Build
from analyse.models import Builds
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases
from analyse.tests.testutil import TestUtils


class BuildTotalPassPercentageTest(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testGenerateTotalPassRate(self):
        Builds.create_builds(TestUtils().connectfour_config(), BuildTotalPassPercentageTest.PATTERN);
        self.assertEqual(2, Build.total('connectfour4'));
        self.assertEqual(1, Build.passed_count('connectfour4'));

    def testGenerateTotalBuilds(self):
        Builds.create_builds(TestUtils().connectfour_config(), BuildTotalPassPercentageTest.PATTERN);
        self.assertEqual(2, Build.total('connectfour4'));

