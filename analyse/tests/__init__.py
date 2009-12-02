import unittest
import doctest
import analyse.tests.build_tests
import analyse.tests.build_factory_tests
import analyse.tests.build_total_pass_percentage_tests
import analyse.tests.successful_rate_chart
import analyse.tests.datetimeutils_tests
import analyse.tests.osutils_tests
import analyse.tests.builds_tests
import analyse.tests.config_tests
import analyse.tests.configs_tests
import analyse.tests.functional_tests
import analyse.tests.perf_tests
import os                                                  

def suite():
    s = unittest.TestSuite()
    test_type = os.environ.get("TEST_TYPE")
    if test_type == 'PERF' :
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.perf_tests.PerfTests))
    else :
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_tests.BuildTest))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_factory_tests.BuildFactoryTest))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_total_pass_percentage_tests.BuildTotalPassPercentageTest))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.successful_rate_chart.SuccessfulRateChartTests))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.datetimeutils_tests.DatetimeUtilsTest))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.builds_tests.BuildsTest))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.config_tests.ConfigTests))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.configs_tests.ConfigsTests))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.osutils_tests.OSUtilsTests))
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.functional_tests.FunctionalTests))
    return s
