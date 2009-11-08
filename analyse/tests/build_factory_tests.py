from django.test import TestCase

from analyse.models import Build
from analyse.models import BuildFactory
import os
from django.conf import settings
from datetime import datetime

class BuildFactoryTest(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testToParseAllTheLogs(self):
        self.assertEqual(2, len(BuildFactory.create_builds("connectfour4", BuildFactoryTest.PATTERN)))

    def testToParseTheInformationCorrectly(self):
        builds = BuildFactory.create_builds("connectfour4", BuildFactoryTest.PATTERN);
        self.assertEqual('connectfour4', builds[0].name)


    def testShouldParseAndPersit(self):
        self.assertEqual(0, len(Build.objects.all()))
        builds = BuildFactory.create_builds("connectfour4", BuildFactoryTest.PATTERN);
        self.assertEqual(2, len(Build.objects.all()))


    def testShouldNotThrowExceptionWhenProcessingXmlFile(self):
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'

        builds = BuildFactory.create_builds("cclive-release-jdk1.5", "log20080624064201Lbuild.70.xml")
        
        self.assertEqual(True, True)
   
    def testShouldFilter1Files(self):
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        files = BuildFactory.filter(self.ccroot, 1)
        self.assertEquals(1, len(files))
        self.assertEquals('log20080924062941.xml', files[0])
    
    def testShouldFilterThe5Files(self):
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        files = BuildFactory.filter(self.ccroot, 5)
        self.assertEquals(5, len(files))
        self.assertEquals('log20080923021338.xml', files[0])
        self.assertEquals('log20080923232508.xml', files[1])
        self.assertEquals('log20080924001513.xml', files[2])
        self.assertEquals('log20080924052506.xml', files[3])
        self.assertEquals('log20080924062941.xml', files[4])