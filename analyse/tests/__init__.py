import unittest
import doctest
import analyse.tests.build_tests
import analyse.tests.build_factory_tests
import analyse.tests.build_total_pass_percentage_tests
import analyse.tests.statistics_generation_tests

def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_tests.BuildTest))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_factory_tests.BuildFactoryTest))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(
            analyse.tests.build_total_pass_percentage_tests.BuildTotalPassPercentageTest))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(
            analyse.tests.statistics_generation_tests.StatisticsGenerationTests))

    return s
