from django.test import TestCase

from analyse.models import Build
from analyse.models import Builds
import os
from django.conf import settings
from datetime import datetime

class BuildFactoryTest(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testToParseAllTheLogs(self):
        self.assertEqual(2, len(Builds.create_builds("connectfour4", BuildFactoryTest.PATTERN, 2)))

    def testToParseTheInformationCorrectly(self):
        builds = Builds.create_builds("connectfour4", BuildFactoryTest.PATTERN, 2);
        self.assertEqual('connectfour4', builds[0].name)


    def testShouldParseAndPersit(self):
        self.assertEqual(0, len(Build.objects.all()))
        builds = Builds.create_builds("connectfour4", BuildFactoryTest.PATTERN, 2);
        self.assertEqual(2, len(Build.objects.all()))


    def testShouldNotThrowExceptionWhenProcessingXmlFile(self):
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'

        builds = Builds.create_builds("cclive-release-jdk1.5", "log20080624064201Lbuild.70.xml", 2)
        
        self.assertEqual(True, True)
   
    def testShouldFilter1Files(self):
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        files = Builds.filter(self.ccroot, 1)
        self.assertEquals(1, len(files))
        self.assertEquals('log20080924062941.xml', files[0])
    
    def testShouldFilterThe5Files(self):
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        files = Builds.filter(self.ccroot, 5)
        self.assertEquals(5, len(files))
        self.assertEquals('log20080923021338.xml', files[0])
        self.assertEquals('log20080923232508.xml', files[1])
        self.assertEquals('log20080924001513.xml', files[2])
        self.assertEquals('log20080924052506.xml', files[3])
        self.assertEquals('log20080924062941.xml', files[4])

    def testShouldOnlyParseThe5Builds(self) :
        self.ccroot = self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        builds = Builds.create_builds(self.ccroot, required_builds = 2)
        self.assertEquals(2, len(builds))
        self.assertEquals(datetime(2008, 9, 24, 5, 25, 6), builds[0].start_time)
        self.assertEquals(datetime(2008, 9, 24, 6, 29, 41), builds[1].start_time)
    