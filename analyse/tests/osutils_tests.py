from django.test import TestCase
import os              
import util.osutils                                     
from django.conf import settings

class OSUtilsTests(TestCase):                               
    def setUp(self):
        self.root = settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        
        
    def testShouldSortTheFilesBasedOnTheRuleAsc(self):
        files = os.sort_by_rule(self.root, 'log([0-9]*).*.xml', 'asc')
        self.assertEquals(55, len(files))
        self.assertEquals('log20080924062941.xml', files[54])
        self.assertEquals('log20080624064201Lbuild.70.xml', files[0])

    def testShouldSortTheFilesBasedOnTheRuleDesc(self):
       files = os.sort_by_rule(self.root, 'log([0-9]*).*.xml', 'desc')
       self.assertEquals('log20080924062941.xml', files[0])
       self.assertEquals('log20080624064201Lbuild.70.xml', files[54])     
                                                                     