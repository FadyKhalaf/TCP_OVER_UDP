'''
Created on Nov 25, 2016

@author: fady
'''

import numpy as np
from matplotlib.mlab import base_repr

def addBit(bit1, bit2, carry):
    bit1 = int(bit1)
    bit2 = int(bit2)
    carry = int(carry)
    return np.binary_repr(bit1+bit2+carry, width=2)

def ngte(n):
    rslt = ""
    for i in n :
        if i == "1":
            rslt += '0'
        elif i == "0" :
            rslt += '1'
    return rslt

def addAndWrapCarry(firstWord, secondWord):
    temp1 = firstWord[::-1]
    temp2 = secondWord[::-1]
    result = ""
    bitresult = addBit(temp1[0], temp2[0], '0')
    result = bitresult[1] + result
    for i in range(1, len(temp1)):
        bitresult = addBit(temp1[i], temp2[i], bitresult[0])
        result = bitresult[1] + result
    if bitresult[0] == '1':
        result = '1' + result
        
    if len(result) > len(temp1):
        return addAndWrapCarry(result[1:], np.binary_repr(1, 16))
    return ngte(result)
        
        

def calculate_checksum(data):
    firstByte = np.binary_repr(ord(data[0]), width=8)
    if len(data) > 4:
        secondByte = np.binary_repr(ord(data[1]), width=8)
        firstWord = firstByte + secondByte
        secondWord  = np.binary_repr(ord(data[3]), width=8) + np.binary_repr(ord(data[4]), width=8)
        return addAndWrapCarry(firstWord, secondWord)
    

def make_pckt(seq_no, data, checksum):
    binData = ""
    for char in data:
        binData += np.binary_repr(ord(char), 8)
    pckt = seq_no + checksum + binData
    return pckt
    
        
def iscorrupted(pck):
    original_checksum = pck[1:17]
    calcualated_checksum = addAndWrapCarry(pck[17:33], pck[25:49])
    return original_checksum != calcualated_checksum

def get_seq_no(pckt):
    return pckt[0]



        
        
        

