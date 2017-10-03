'''
Created on Nov 25, 2016

@author: fady
'''
'''
Created on Nov 24, 2016

@author: fady
'''

from socket import socket, AF_INET, SOCK_DGRAM
import threading
import time

from common import calculate_checksum, make_pckt, iscorrupted, get_seq_no
from config import UDP_IP, UDP_PORT


class sender(threading.Thread):
    TIMEOUT = 1
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.seq_num = 0
        self.Ack = 0
        self.sock = sock
        self.timer = None
        self.sentpckt = None
        self.states = {'send0':3 , 'ack0':0, 'send1':4, 'ack1':1};
        self.state = self.states['send0']
        
    
    def send(self, data):
        if self.state == self.states['send0']:
            self.sentpckt = make_pckt('0', data, calculate_checksum(data))
            self.sock.send(self.sentpckt)
            self.state = self.states['ack0']
            self.timer = threading.Timer(sender.TIMEOUT, sender.timed_out, (self,))
            self.timer.start()
        if self.state == self.states['send1']:
            sentpckt = make_pckt('1', data, calculate_checksum(data))
            self.sock.send(sentpckt)
            self.state = self.states['ack1']
            self.timer = threading.Timer(sender.TIMEOUT, sender.timed_out, (self,))
            self.timer.start()
            
    def recv(self, ack):
        if iscorrupted(ack):
            print("packet is corrupted")
        else:
            num = get_seq_no(ack)
            if num == '0':
                if self.state == self.states['ack0']:
                    self.timer.cancel()
                else :
                    print "recieved ack1 instead of ack0"
            elif num == '1':
                if self.state == self.states['ack1']:
                    self.timer.cancel()
                else:
                    print "recieved ack0 instead of ack1"
                    
    def timed_out(self):
        self.sock.send(self.sentpckt)
        self.timer = threading.Timer(sender.TIMEOUT, sender.timed_out, (self,))
        print "timeout"
            
    def run(self):
        while True:
            pkt = self.sock.recv(1024)
            self.recv(pkt)

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.connect((UDP_IP, UDP_PORT))
    Sender = sender(sock)
    Sender.start()
    for i in range(32):
        Sender.send('hello' + str(i))
        time.sleep(1)
    