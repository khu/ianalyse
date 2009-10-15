from django.test import TestCase

from analyse.models import Build
from analyse.models import BuildFactory
import os
from django.conf import settings
from datetime import datetime

class BuildFactoryTest(TestCase):
    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures/connectfour4'

    def testToParseAllTheLogs(self):
        self.assertEqual(2, len(BuildFactory.create_builds()))

    def testToParseTheInformationCorrectly(self):
        builds = BuildFactory.create_builds();
        self.assertEqual('connectfour4', builds[0].name)

    def testShouldParseAndPersit(self):
        self.assertEqual(0, len(Build.objects.all()))
        builds = BuildFactory.create_builds();
        self.assertEqual(2, len(Build.objects.all()))


