'''
Created on Nov 25, 2016

@author: fady
'''
import random
from socket import socket, SOCK_DGRAM, AF_INET
import threading

from common import calculate_checksum, iscorrupted, make_pckt, get_seq_no
from config import UDP_IP, UDP_PORT


class receiver(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.expected_seq_num = '0'
        self.sock = sock
        self.sentpckt = None
        self.Ack = "Ack00"
        
    def recv(self, pckt, dest):
        if iscorrupted(pckt):
            pck = make_pckt(self.expected_seq_num, self.Ack, calculate_checksum(self.Ack))
            self.sock.sendTo(pck, dest)
        else :
            num = get_seq_no(pckt)
            if num == self.expected_seq_num:
                #pckt recieved
                self.deliver_data("recieved")
                if self.expected_seq_num ==  '0':
                    self.expected_seq_num = '1'
                else :
                    self.expected_seq_num = '0'
    def run(self):
        while True:
            pckt, dest = self.sock.recvfrom(2048)
            while random.random() > 0.4: #emulate 40% loss
                self.recv(pckt, dest)
    def deliver_data(self, data):
        print data
                
if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    receiver = receiver(sock)
    receiver.start()
                
        
        