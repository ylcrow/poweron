'''@author: lockrecv@gmail.com'''

class Server:
    '''Power On State Server'''

    def __init__(self, ip, port, domain, administrator):        
        self.ip = ip
        self.port = port
        self.domain = domain
        self.administrator = administrator