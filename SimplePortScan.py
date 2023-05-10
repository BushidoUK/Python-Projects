#!/usr/bin/python

import socket as sk
	for port in range(1,1024): #The Range of Ports Scanned
		try:
			s=sk.socket(sk.AF_INET,sk.SOCK_STREAM) #Address Family IPv4 and TCP Socket
			s.settimeout(1000) #Scan for 1000 seconds
			s.connect(('127.0.0.1',port)) #Localhost is the default IP to be scanned from Port 1-1024
			print '%d:OPEN' % (port) #The open ports are printed to the console
			s.close
		except: continue
