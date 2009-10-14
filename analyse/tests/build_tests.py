import unittest

from analyse.models import Build
import os
from django.conf import settings
from datetime import datetime


class BuildTest(unittest.TestCase):
    PASSED_LOG = '''<cruisecontrol>
  <modifications />
  <info>
    <property name="projectname" value="connectfour4" />
    <property name="lastbuild" value="20091011000000" />
    <property name="lastsuccessfulbuild" value="20091011000000" />
    <property name="builddate" value="2009-10-11T09:39:22" />
    <property name="cctimestamp" value="20091011173922" />
    <property name="label" value="build.1" />
    <property name="interval" value="300" />
    <property name="lastbuildsuccessful" value="true" />
    <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
    <property name="logfile" value="log20091011173922Lbuild.1.xml" />
  </info>
  <build time="0 minute(s) 0 second(s)">
    <target name="exec">
      <task name="echo">
        <message priority="info"><![CDATA[haha]]></message>
      </task>
    </target>
  </build>
</cruisecontrol>'''

    FAILED_LOG = '''<?xml version="1.0" encoding="UTF-8"?>
<cruisecontrol>
  <modifications>
    <modification type="mercurial">
      <file action="added">
        <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
        <filename>b</filename>
      </file>
      <date>2009-10-11T09:48:27</date>
      <user>twer@localhost</user>
      <comment><![CDATA[fucked]]></comment>
      <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
    </modification>
    <modification type="mercurial">
      <file action="modified">
        <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
        <filename>b</filename>
      </file>
      <date>2009-10-11T09:48:27</date>
      <user>twer@localhost</user>
      <comment><![CDATA[fucked]]></comment>
      <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
    </modification>
  </modifications>
  <info>
    <property name="projectname" value="connectfour4" />
    <property name="lastbuild" value="20091011201149" />
    <property name="lastsuccessfulbuild" value="20091011201149" />
    <property name="builddate" value="2009-10-13T14:03:24" />
    <property name="cctimestamp" value="20091013220324" />
    <property name="label" value="build.18" />
    <property name="interval" value="300" />
    <property name="lastbuildsuccessful" value="true" />
    <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
    <property name="logfile" value="log20091013220324.xml" />
  </info>
  <build time="0 minute(s) 0 second(s)" error="exec error">
    <target name="exec">
      <task name="echa">
        <message priority="error"><![CDATA[Could not execute command: echa with arguments: haha]]></message>
      </task>
    </target>
  </build>
</cruisecontrol>'''


    def setUp(self):
        self.root = settings.PROJECT_DIR

    def testToParseTheProjectName(self):
        build = Build.from_xml(BuildTest.FAILED_LOG)
        self.assertEqual("connectfour4", build.name)

    def testToParseThePassLogForBuildNumber(self):
        build = Build.from_xml(BuildTest.PASSED_LOG)
        self.assertEqual("build.1", build.number)

    def testToParseThePassFailedLogForBuildNumber(self):
        build = Build.from_xml(BuildTest.FAILED_LOG)
        self.assertEqual("build.18", build.number)

    def testToParseThePassFailedLogForResult(self):
        build = Build.from_xml(BuildTest.FAILED_LOG)
        self.assertEqual(False, build.passed)

    def testToParseThePassPassedLogForResult(self):
        build = Build.from_xml(BuildTest.PASSED_LOG)
        self.assertEqual(True, build.passed)

    def testToParseTheFailedLogForBuildDate(self):
        expecteddate = datetime(2009, 10, 11, 17, 39, 22);
        build = Build.from_xml(BuildTest.PASSED_LOG)
        self.assertEqual(expecteddate, build.start_time)

    def testToParseTheFailedLogForBuildDate(self):
        expecteddate = datetime(2009, 10, 11, 20, 11, 49);
        build = Build.from_xml(BuildTest.FAILED_LOG)
        self.assertEqual(expecteddate, build.last_pass)
        

    #dt= datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
