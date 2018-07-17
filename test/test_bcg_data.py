#!/usr/bin/env python
import ssdp_search
import socket
import re
import datetime
 
 
#data format Time, HR, RR, SV, HRV, Signal Strength, Status, B2B, B2B', B2B''.
 
TCP_IP      = '192.168.24.14'
TCP_PORT    = 8080
BUFFER_SIZE = 1024
MESSAGE = "BCG Client!"
# 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('USER: admin')
s.send('PASS: admin')
print(MESSAGE)


 
old_timestamp = datetime.datetime.now()

while 1:
   data = s.recv(BUFFER_SIZE)
  # print (data)
   [Time,HR,RR,SV,HRV,SS,Status,BB1,BB2,BB3]=data.split(',')
   
   HeartRate  = int(HR)
   TimeSensor_ms = int(Time)
   timestamp = datetime.datetime.now()
   print "ServerTime:"+ timestamp.strftime('%Y%m%d-%H%M%S-%f') + " Time %s Your HR is % d" % (Time, HeartRate)
   
   
   delta_time    = timestamp - old_timestamp;
   old_timestamp = timestamp
   #print (delta_time)
   if ( delta_time >  datetime.timedelta(seconds=1.5)):
         print("Error")
         
      
s.close() 


