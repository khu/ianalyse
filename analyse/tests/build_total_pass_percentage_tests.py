from django.test import TestCase
from analyse.models import Build
from analyse.models import BuildFactory
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases

class BuildTotalPassPercentageTest(TestCase):
    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures/connectfour4'

    def testGenerateTotalPassRate(self):
        BuildFactory.create_builds();
        self.assertEqual(2, Build.total('connectfour4'));
        self.assertEqual(1, Build.passed_count('connectfour4'));

    def testGenerateTotalBuilds(self):
        BuildFactory.create_builds();
        self.assertEqual(2, Build.total('connectfour4'));

