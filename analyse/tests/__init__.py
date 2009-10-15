import unittest
import doctest
import analyse.tests.build_tests
import analyse.tests.build_factory_tests
import analyse.tests.build_total_pass_percentage_tests

def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_tests.BuildTest))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.build_factory_tests.BuildFactoryTest))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(
            analyse.tests.build_total_pass_percentage_tests.BuildTotalPassPercentageTest))
    return s
