import unittest
import doctest
import analyse.tests.tests

def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.tests.BuildTest))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(analyse.tests.tests.BuildFactoryTest))
    return s
