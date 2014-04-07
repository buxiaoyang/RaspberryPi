#! /usr/bin/python
from __future__ import division
from subprocess import PIPE, Popen
import ST7565
import time
import socket 
import fcntl 
import struct 
import sys
import psutil

def main():
	ST7565.io_init()
	ST7565.lcd_init()	
	ST7565.lcd_chinese(0,0,7)
	ST7565.lcd_chinese(16,0,8)
	ST7565.lcd_ascii168(32,0,10)
	
	ST7565.lcd_ascii168(0,4,44); #C
	ST7565.lcd_ascii168(8,4,57); #P
	ST7565.lcd_ascii168(16,4,62); #U
	ST7565.lcd_ascii168(24,4,10); #:
	ST7565.lcd_ascii168(64,4,11); #%
	

	ST7565.lcd_chinese(80,4,9);
	ST7565.lcd_chinese(96,4,10);
	ST7565.lcd_ascii168(112,4,10);
	
	ST7565.lcd_ascii168(0,6,59); #R
	ST7565.lcd_ascii168(8,6,42); #A
	ST7565.lcd_ascii168(16,6,54); #M
	ST7565.lcd_ascii168(24,6,10); #:
	ST7565.lcd_ascii168(64,6,11); #%
	
	ST7565.lcd_chinese(104,6,11);
	
	while True:
		updateDisplay()
		time.sleep(10)
	
	
def updateDisplay():

	#Update Time
	timeString = time.strftime('%H:%M',time.localtime(time.time()))
	timeStringLen = len(timeString)	
	for i in range(0, timeStringLen):
		if timeString[i] == ':':
			ST7565.lcd_ascii168(48+i*8,0,10)
		else:
			ST7565.lcd_ascii168(48+i*8,0,int(timeString[i]))

	#Update net work flag
	ipString = ''
	netcard = 0
	try:
		ipString = get_local_ip('eth0')
		netcard = 0
	except:
		try:
			ipString = get_local_ip('wlan0')
			netcard = 1
		except:
			netcard = 2
	if netcard == 0:
		ST7565.lcd_ascii168(96,0,20)
		ST7565.lcd_ascii168(104,0,35)
		ST7565.lcd_ascii168(112,0,23)
		ST7565.lcd_ascii168(120,0,0)
	elif netcard == 1:
		ST7565.lcd_ascii168(96,0,38)
		ST7565.lcd_ascii168(104,0,24)
		ST7565.lcd_ascii168(112,0,21)
		ST7565.lcd_ascii168(120,0,24)
	else:
		ST7565.lcd_ascii168(96,0,29)
		ST7565.lcd_ascii168(104,0,30)
		ST7565.lcd_ascii168(112,0,29)
		ST7565.lcd_ascii168(120,0,20)
		
	#Update IP address
	ipStringLen = len(ipString)	
	for i in range(0, ipStringLen):
		if ipString[i] == '.':
			ST7565.lcd_ascii168(i*8,2,15)
		else:
			ST7565.lcd_ascii168(i*8,2,int(ipString[i]))
	#Update CPU usage
	cpu_usage = psutil.cpu_percent()
	cpu_usage = int(cpu_usage)
	
	ST7565.lcd_ascii168(40,4,int(cpu_usage/100));
	ST7565.lcd_ascii168(48,4,int(cpu_usage%100/10));
	ST7565.lcd_ascii168(56,4,int(cpu_usage%10));
	
	#Update RAM usage
	ram = psutil.phymem_usage().percent
	ram = int(ram)
	
	ST7565.lcd_ascii168(40,6,int(ram/100));
	ST7565.lcd_ascii168(48,6,int(ram%100/10));
	ST7565.lcd_ascii168(56,6,int(ram%10));
	
	#Update Temperature
	cpu_temperature = get_cpu_temperature()
	cpu_temperature = int(cpu_temperature)
	
	ST7565.lcd_ascii168(80,6,int(cpu_temperature/100)); 
	ST7565.lcd_ascii168(88,6,int(cpu_temperature%100/10));
	ST7565.lcd_ascii168(96,6,int(cpu_temperature%10));

def get_local_ip(ethname):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = fcntl.ioctl(sock.fileno(), 0x8915, struct.pack('256s', ethname))
        return socket.inet_ntoa( addr[20:24] )
        
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])
    
main()