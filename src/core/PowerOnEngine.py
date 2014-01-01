'''@author: lockrecv@gmail.com'''

from src.util.PowerOn import PowerOn

class PowerOnEngine:
    '''Power On State Engine'''

    def __init__(self):
        self.powerOn = PowerOn('config/power-on.json')

    def run(self):
        pass