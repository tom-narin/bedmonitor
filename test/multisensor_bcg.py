#!/usr/bin/env python
import socket
import time
 
 
#data format Time, HR, RR, SV, HRV, Signal Strength, Status, B2B, B2B', B2B''.
 
TCP_IP_01 = '192.168.1.55'
TCP_IP_02 = '192.168.1.60'


TCP_PORT = 8080
BUFFER_SIZE = 1024
MESSAGE = "BCG Client!"
 
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP_01, TCP_PORT))
s1.send('USER: admin')
s1.send('PASS: admin')

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((TCP_IP_02, TCP_PORT))
s2.send('USER: admin')
s2.send('PASS: admin')




print(MESSAGE)
 


while 1:
   data_01 = s1.recv(BUFFER_SIZE)
   data_02 = s2.recv(BUFFER_SIZE)
   print ('Time, HR, RR, SV, HRV, SS, Status, BB1, BB2, BB3')
   print ("SenSor01:" ,data_01)
   print ("SenSor02:" ,data_02)
   time.sleep(0.1)
 
s.close() 