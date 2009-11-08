from django.test import TestCase

from analyse.models import Build, Builds
import os
from django.conf import settings
from datetime import datetime
import util.datetimeutils

class BuildsTest(TestCase):
    PASSED_LOG_AT_OCT_11 = '''<cruisecontrol>
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
  <build time="1 minute(s) 0 second(s)">
    <target name="exec">
      <task name="echo">
        <message priority="info"><![CDATA[haha]]></message>
      </task>
    </target>
  </build>
</cruisecontrol>'''
    ANOTHER_PASSED_LOG_AT_OCT_11 = '''<cruisecontrol>
  <modifications />
  <info>
    <property name="projectname" value="connectfour4" />
    <property name="lastbuild" value="20091011000000" />
    <property name="lastsuccessfulbuild" value="20091011000000" />
    <property name="builddate" value="2009-10-11T10:39:22" />
    <property name="cctimestamp" value="20091011173900" />
    <property name="label" value="build.1" />
    <property name="interval" value="300" />
    <property name="lastbuildsuccessful" value="true" />
    <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
    <property name="logfile" value="log20091011173922Lbuild.1.xml" />
  </info>
  <build time="0 minute(s) 2 second(s)">
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
  <build time="0 minute(s) 4 second(s)" error="exec error">
    <target name="exec">
      <task name="echa">
        <message priority="error"><![CDATA[Could not execute command: echa with arguments: haha]]></message>
      </task>
    </target>
  </build>
</cruisecontrol>'''

    def setUp(self):
        self.root                     = settings.PROJECT_DIR
        self.failed                   = Build.from_xml(BuildsTest.FAILED_LOG)
        self.passed_at_oct_11         = Build.from_xml(BuildsTest.PASSED_LOG_AT_OCT_11)
        self.another_passed_at_oct_11 = Build.from_xml(BuildsTest.ANOTHER_PASSED_LOG_AT_OCT_11)

    def testShouldGroupTheBuilds(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed]
        grouped_builds = builds.group_by_each_day()
        self.assertEquals(2, len(grouped_builds))

        atime = datetime.strptime("20091011000000", "%Y%m%d%H%M%S")
        btime = datetime.strptime("20091013000000", "%Y%m%d%H%M%S")

        self.assertEquals(2, len(grouped_builds[atime].builds))
        btime = datetime.strptime("20091013000000", "%Y%m%d%H%M%S")
        self.assertEquals(1, len(grouped_builds[btime].builds))

    def testShouldCalculateThePassCount(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed]

        atime = datetime.strptime("20091011000000", "%Y%m%d%H%M%S")
        self.assertEquals(2, builds.group_by_each_day()[atime].pass_count())

    def testShouldCalculateTheFailCount(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed]

        atime = datetime.strptime("20091013000000", "%Y%m%d%H%M%S")
        self.assertEquals(0, builds.group_by_each_day()[atime].pass_count())

    def testShouldCalculateThePassRate(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed]

        atime = datetime.strptime("20091011000000", "%Y%m%d%H%M%S")
        self.assertEquals(1, builds.group_by_each_day()[atime].pass_rate())

    def testShouldTheBuildsTimes(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed]

        atime = datetime.strptime("20091011000000", "%Y%m%d%H%M%S")
        values, min, max, max_time = builds.build_times()
        self.assertEquals(3, len(values))

        self.assertEquals (util.datetimeutils.cctimestamp_to_unix_timestamp("20091011173900"), min)
        self.assertEquals (util.datetimeutils.cctimestamp_to_unix_timestamp("20091013220324"), max)
        self.assertEquals (60, max_time)

    def testShouldCalculateTheBuildPerDay(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed]

        values, labels, max_time = builds.per_build_time()
        
        self.assertEquals('#1C9E05', values[0]['colour']);
        self.assertEquals('#1C9E05', values[1]['colour']);
        self.assertEquals('#FF368D', values[2]['colour']);
        self.assertEquals(60, values[0]['top']);
        self.assertEquals(2,  values[1]['top']);
        self.assertEquals(4,  values[2]['top']);
        self.assertEquals('2009-10-11 17:39:22', labels[0])
        self.assertEquals('2009-10-11 17:39:00', labels[1])
        self.assertEquals('2009-10-13 22:03:24', labels[2])
        self.assertEquals(60, max_time);



