from django.test import TestCase
from analyse.tests.testutil import TestUtils
from django.test.client import Client

class FunctionalTests(TestCase):

    def setUp(self):
        self.test_utils = TestUtils()
        self.test_utils.cleanup_results()
        

    def test_user_should_be_able_to_setup_the_application(self):
        user = User()
        user.open_home_page()
        print user.response
        self.assertContains(user.response, 'Did you configure this file properly')
        self.assertContains(user.response, user.found_config_file_location())
        user.generates_reports_for('connectfour4')

        user.downloads_build_times_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_csv()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_pass_rate_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_per_build_time_data()
        self.assertEquals(True, user.can_visit_resource())
    
    def test_user_should_not_wait_for_re_generating_the_data_when_referesh_the_page(self):
        user = User()
        user.open_home_page()
        user.generates_reports_for('connectfour4')
        
        before = self.test_utils.last_modified_on('connectfour4')
        user.open_home_page()        
        after = self.test_utils.last_modified_on('connectfour4')        

        self.assertEquals(before, after)
        
class User :
    def __init__(self):
        self.client = Client()
        
    def open_home_page(self):
        self.response = self.client.get('/analyse/index.html', follow=True)

               
    
    def found_config_file_location(self):
        return self.response.context['config_file']
    
    def found_pass_rate(self):
        return self.response.context['config_file']
    
    def generates_reports_for(self, name):
        self.response = self.client.post('/analyse/generate.html', {})
        self.project_name = name
    
    def downloads_build_times_data(self):
        self.response = self.client.get('/results/' + self.project_name + '/build_times.txt')
        
    def downloads_csv(self):
        self.response = self.client.get('/results/' + self.project_name + '/connectfour4.csv')
        
    def downloads_pass_rate_data(self):
        self.response = self.client.get('/results/' + self.project_name + '/pass_rate.txt')        

    def downloads_per_build_time_data(self):
        self.response = self.client.get('/results/' + self.project_name + '/per_build_time.txt')
        
    def downloads_successful_rate_data(self):
        self.response = self.client.get('/results/' + self.project_name + '/successful_rate.txt')        

    def can_visit_resource(self):
        code = self.response.status_code
        return code >= 200 and code < 300
    