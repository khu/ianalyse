from django.test import TestCase

from analyse.models import Build
import os
import util.datetimeutils
from django.conf import settings
from datetime import datetime
import time

class DatetimeUtilsTest(TestCase):

    def setUp(self):
        self.root = settings.PROJECT_DIR

    def testShouldReturn3WeeksAndIgnoreHourMinutesSecondsFromSpecifiedTime(self):
        thirtySep = datetime.strptime("20090930070001", "%Y%m%d%H%M%S")
        eighthSep = datetime.strptime("20090909000000", "%Y%m%d%H%M%S")

        self.assertEquals(eighthSep, util.datetimeutils.days_ago(21, thirtySep))

    def testShouldReturn3WeeksAgoIfSpecifyVeryOldDate(self):
        thirtySep = datetime.strptime("20090930070001", "%Y%m%d%H%M%S")
        eighthSep = datetime.strptime("20090909000000", "%Y%m%d%H%M%S")
        veryold = datetime.strptime("20080909000000", "%Y%m%d%H%M%S")

        self.assertEquals(eighthSep, util.datetimeutils.days_ago_not_before(21, thirtySep, veryold))

    def testShouldReturnNow(self):
        thirtySep = datetime.strptime("20090930070001", "%Y%m%d%H%M%S")
        eighthSep = datetime.strptime("20090909000000", "%Y%m%d%H%M%S")
        quiteNew =  datetime.strptime("20090927013000", "%Y%m%d%H%M%S")

        self.assertEquals(quiteNew, util.datetimeutils.days_ago_not_before(21, thirtySep, quiteNew))

    def testShouldEvaluateTheSecondsToSeconds(self):
        self.assertEquals(1, util.datetimeutils.evaluate_time_to_seconds("0 minute(s) 1 second(s)"))

    def testShouldEvaluateTheMinutesToSeconds(self):
        self.assertEquals(61, util.datetimeutils.evaluate_time_to_seconds("1 minute(s) 1 second(s)"))

    def testShouldEvaluateTheHoursToSeconds(self):
        self.assertEquals(3661, util.datetimeutils.evaluate_time_to_seconds("1 hour(s) 1 minute(s) 1 second(s)"))