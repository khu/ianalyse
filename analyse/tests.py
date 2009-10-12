import unittest

from analyse.models import Build

class SimpleTest(unittest.TestCase):
    def testToRomanKnownValues(self):
            print Build.from_xml()
            self.assertEqual(1, 1)

    def testToRomanKnownValues1(self):
            self.assertEqual(1, 1)

    def testToRomanKnownValues2(self):
            self.assertEqual(1, 1)
