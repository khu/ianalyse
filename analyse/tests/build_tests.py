from django.test import TestCase

from analyse.models import Build
import os
from django.conf import settings
from datetime import datetime
from analyse.tests.testutil import TestUtils
from analyse.config import Config, Configs

class BuildTest(TestCase):

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + '/analyse/tests/fixtures/connectfour4'

    def testToParseTheProjectName(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual("connectfour4", build.name)

    def testToParseThePassLogForBuildNumber(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual("build.1", build.number)

    def testToParseTheFailedLogForBuildNumber(self):
        build = Build.from_file(self.ccroot + '/log20091013220324.xml')
        self.assertEqual("build.18", build.number)

    def testToParseThePassFailedLogForResult(self):
        build = Build.from_file(self.ccroot + '/log20091013220324.xml')
        self.assertEqual(False, build.is_passed)

    def testToParseThePassPassedLogForResult(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual(True, build.is_passed)

    def testToParseTheFailedLogForBuildDate(self):
        expecteddate = datetime(2009, 10, 11, 17, 39, 22);
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual(expecteddate, build.start_time)

    def testToParseTheFailedLogForBuildDate(self):
        expecteddate = datetime(2009, 10, 11, 20, 11, 49);
        build = Build.from_file(self.ccroot + '/log20091013220324.xml')
        self.assertEqual(expecteddate, build.last_pass)
    
    def testToSelectValuesAsArrayByApplyingXPath(self):
        file = self.ccroot + '/log20091011173922Lbuild.1.xml'
        config = Configs().find('connectfour4')
        values = Build.select_values(file, config.csv_settings())
        self.assertEquals('connectfour4', values[0])
        self.assertEquals('1 minute(s) 0 second(s)', values[2])
        self.assertEquals('build.1', values[1])
        self.assertEquals(None, values[3])
