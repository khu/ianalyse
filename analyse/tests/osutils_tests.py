from django.test import TestCase
import os              
import util.osutils                                     
from django.conf import settings

class OSUtilsTests(TestCase):                               
    def setUp(self):
        self.root = settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        
        
    def testShouldSortTheFilesBasedOnTheRuleDES(self):
        files = os.sort_by_rule(self.root, 'log([0-9]*).*.xml')
        self.assertEquals(55, len(files))

    def testShouldSortTheFilesBasedOnTheRuleASC(self):
        pass