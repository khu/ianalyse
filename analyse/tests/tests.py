import unittest

from analyse.models import Build
import os
from django.conf import settings

class BuildTest(unittest.TestCase):
    FIRST_PASSED_LOG = '''<cruisecontrol>
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

    def setUp(self):
        self.root = settings.PROJECT_DIR

    def testToRomanKnownValues(self):
        build = Build.from_xml(BuildTest.FIRST_PASSED_LOG)

        self.assertEqual(1, build.number)


    def testToRomanKnownValues1(self):
        self.assertEqual(1, 1)

    def testToRomanKnownValues2(self):
        self.assertEqual(1, 1)
