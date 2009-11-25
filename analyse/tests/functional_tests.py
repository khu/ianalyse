from django.test import TestCase
from analyse.tests.testutil import TestUtils
from django.test.client import Client

class FunctionalTests(TestCase):

    def setUp(self):
        self.test_utils = TestUtils()
        self.test_utils.cleanup_results()

    def tearDown(self):
        self.test_utils.cleanup_results()

    def test_user_should_be_able_to_setup_the_application(self):
        user = User()
        user.open_home_page()
        self.assertContains(user.response, 'Missing Data')
        user.open_show_page('connectfour4')
        self.assertContains(user.response, 'MISSING REPORT')
        self.assertContains(user.response, user.found_config_file_location())
        user.generates_reports_for('connectfour4')

        user.open_setup_page('connectfour4')
        self.assertContains(user.response, 'OK')

        user.downloads_build_times_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_csv()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_pass_rate_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_per_build_time_data()
        self.assertEquals(True, user.can_visit_resource())
    
    def test_user_should_be_able_to_request_with_project_id(self):
        user = User()
        user.open_home_page()
        self.assertContains(user.response, 'Missing Data')
        user.open_show_page('cclive')       
        self.assertContains(user.response, 'MISSING REPORT')
        self.assertContains(user.response, user.found_config_file_location())
        user.generates_reports_for('cclive')

        user.open_setup_page('cclive')
        self.assertContains(user.response, 'OK')
        
        user.open_show_page('cclive')

        self.assertContains(user.response, '4 runs')
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

    def open_show_page(self, id):
        self.response = self.client.get('/analyse/show.html?id=' + id, follow=True)

    def open_setup_page(self, id):
        self.response = self.client.get('/analyse/setup.html?id=' + id, follow=True)
    
    def found_config_file_location(self):
        return self.response.context['current'].abspath()
    
    def found_pass_rate(self):
        return self.response.context['config_file']
    
    def generates_reports_for(self, id):
        self.response = self.client.post('/analyse/generate.html', {'id' : id}, follow=True)
        self.project_id = id
    
    def downloads_build_times_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/build_times.txt')
        
    def downloads_csv(self):
        self.response = self.client.get('/results/' + self.project_id + '/' + self.project_id + '.csv')
        
    def downloads_pass_rate_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/pass_rate.txt')        

    def downloads_per_build_time_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/per_build_time.txt')
        
    def downloads_successful_rate_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/successful_rate.txt')        

    def can_visit_resource(self):
        code = self.response.status_code
        return code >= 200 and code < 300
    