'''@author: lockrecv@gmail.com'''

import unittest
from src.thirdparty.Ping import Ping

class Test(unittest.TestCase):

    def setUp(self):
        self.ping = Ping()

    def tearDown(self):
        pass

    def testPingVerboseOk(self):
        assert(True)
        self.ping.verbose_ping('www.google.com')
        self.ping.verbose_ping('74.125.128.105')
        self.ping.verbose_ping('www.baidu.com')
        self.ping.verbose_ping('115.239.210.27')
        self.ping.verbose_ping('localhost')        
    
    def testPintVerboseFailed(self):
        assert(True)
        self.ping.verbose_ping('www.does-not-exist-website.com')
        self.ping.verbose_ping('www.another-does-not-exist-website.com')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()