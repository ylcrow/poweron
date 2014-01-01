'''@author: lockrecv@gmail.com'''

import unittest
from src.util.PowerOn import PowerOn 

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        poweron = PowerOn("../../src/config/power-on.json")
        poweron.toString()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()