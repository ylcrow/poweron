'''
@author: lockrecv@gmail.com

A pure python ping implementation using raw socket.

Note that ICMP messages can only be sent from processes running as root.

Inspired by Matthew Dixon Cowles <http://www.visi.com/~mdc/>.
'''

import os
import select
import socket
import struct
import time

class Ping:
    ''' Power On State Pint Utility (3rdparty)'''
    
    def __init__(self):
        self.ICMP_ECHO_REQUEST = 8
    
    def checksum(self, source_string):
        summ = 0
        count_to = (len(source_string)/2)*2
        for count in xrange(0, count_to, 2):
            this = ord(source_string[count+1]) * 256 + ord(source_string[count])
            summ = summ + this
            summ = summ & 0xffffffff
        
        if count_to < len(source_string):
            summ = summ + ord(source_string[len(source_string)-1])
            summ = summ & 0xffffffff
        
        summ = (summ >> 16) + (summ & 0xffff)
        summ = summ + (summ >> 16)
        answer = ~summ
        answer = answer & 0xffff
        
        # Swap bytes
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer
    
    def receive_one_ping(self, my_socket, idd, timeout):
        '''Receive the ping from the socket'''
        time_left = timeout
        while True:
            started_select = time.time()
            what_ready = select.select([my_socket], [], [], time_left)
            how_long_in_select = (time.time() - started_select)
            if what_ready[0] == []: # Timeout
                return
            
            time_received = time.time()
            received_packet, addr = my_socket.recvfrom(1024)
            icmpHeader = received_packet[20:28]
            type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmpHeader)
            
            if packet_id == idd:
                bytess = struct.calcsize("d")
                time_sent = struct.unpack("d", received_packet[28:28 + bytess])[0]
                return time_received - time_sent
            
            time_left = time_left - how_long_in_select
            if time_left <= 0:
                return
        
    def send_one_ping(self, my_socket, dest_addr, idd, psize):
        '''Send one ping to the given address'''
        dest_addr = socket.gethostbyname(dest_addr)
        
        # Remove header size from packet size
        psize = psize - 8
        
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        my_checksum = 0
        
        # Make a dummy header with a 0 checksum
        header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, my_checksum, idd, 1)
        bytess = struct.calcsize("d")
        data = (psize - bytess) * "Q"
        data = struct.pack("d", time.time()) + data
        
        # Calculate the checksum on the data and the dummy header
        my_checksum = self.checksum(header+data)
        
        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy
        header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), idd, 1)
        
        packet = header + data
        my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1
        
    def do_one(self, dest_addr, timeout, psize):
        '''Returns either the delay (in seconds) or none on timeout'''
        icmp = socket.getprotobyname("icmp")
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.errno, (errno, msg):
            if errno == 1:
                # Operation not permitted
                msg = msg + (
                             " - Note that ICMP messages can only be sent from processes"
                             " running as root."
                             )
                raise socket.error(msg)
        
        my_id = os.getpid() & 0xFFFF
        self.send_one_ping(my_socket, dest_addr, my_id, psize)
        delay = self.receive_one_ping(my_socket, my_id, timeout)
        
        my_socket.close()
        return delay
    
    def verbose_ping(self, dest_addr, timeout = 2, count = 4, psize = 64):
        '''
        Send 'count' ping with 'psize' size to 'dest_addr' with
        the given 'timeout' and display the result
        '''
        for i in xrange(count):
            print 'ping %s with ...' % dest_addr
            try:
                delay = self.do_one(dest_addr, timeout, psize)
            except socket.gaierror, e:
                print 'FAILED. (socket error: "%s")' % e[1]
                break
            
            if delay == None:
                print 'FAILED. (timeout within %ssec.)' % timeout
            else:
                delay = delay * 1000
                print 'get ping in %0.4fms' % delay
        print
    
    def quiet_ping(self, dest_addr, timeout = 2, count = 4, psize = 64):
        '''
        Send 'count' pint with 'psize' size to 'dest_addr' with
        the given 'timeout' and display the result.
        Returns 'percent' lost packages, 'max' round trip time
        and 'avg' round trip time.
        '''
        mrtt = None
        artt = None
        
        plist = []
        
        for i in xrange(count):
            try:
                delay = self.do_one(dest_addr, timeout, psize)
            except socket.gaierror, e:
                print 'FAILED. (socket error: "%s")' % e[1]
                break
            
            if delay != None:
                delay = delay * 1000
                plist.append(delay)
        
        # Find lost package percent
        percent_lost = 100 - (len(plist)*100/count)
        
        # Find max and avg round trip time
        if plist:
            mrtt = max(plist)
            artt = sum(plist)/len(plist)
        
        return percent_lost, mrtt, artt