'''@author: lockrecv@gmail.com'''

import json
from src.domain.Server import Server

class PowerOn:
    '''Power On Configuration Utility'''

    def __init__(self, cfile):
        self.system_email = None
        self.system_cc = []
        self.monitor_servers = []
        self.load(cfile)

    def load(self, cfile):
        cf = open(cfile)
        data = json.load(cf)
        
        email_json = data["email"]
        self.system_email = email_json["system-email"]
        for cc in email_json["system-cc"]:
            self.system_cc.append(cc)

        for s in data["monitor-servers"]:
            server = Server(s["ip"], s["port"], s["domain"], s["administrator"])
            self.monitor_servers.append(server)

    def toString(self):
        print self.system_email
        for cc in self.system_cc:
            print cc
        for server in self.monitor_servers:
            print server.ip
            print server.port
            print server.domain
            print server.administrator
            