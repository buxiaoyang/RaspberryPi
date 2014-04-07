#! /usr/bin/python

import RPi.GPIO as GPIO
import Fonts

LCD_CS = 2
LCD_RST  = 3
LCD_A0 = 4
LCD_CLK = 27
LCD_SI = 17

def io_init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(LCD_CS, GPIO.OUT)
	GPIO.setup(LCD_RST, GPIO.OUT)
	GPIO.setup(LCD_A0, GPIO.OUT)
	GPIO.setup(LCD_CLK, GPIO.OUT)
	GPIO.setup(LCD_SI, GPIO.OUT)

def lcd_chinese(xPos, yPos, char):
	lcd_set_page(yPos,xPos)
	for i in range(0, 16): 
		lcd_tranfer_data(Fonts.FONT1616[char][i],1)
	lcd_set_page(yPos+1,xPos)	
	for i in range(16, 32): 
		lcd_tranfer_data(Fonts.FONT1616[char][i],1)

def lcd_ascii168(xPos, yPos, char):
	lcd_set_page(yPos,xPos)
	for i in range(0, 8): 
		lcd_tranfer_data(Fonts.ASCII168[char][i],1)
	lcd_set_page(yPos+1,xPos)	
	for i in range(8, 16): 
		lcd_tranfer_data(Fonts.ASCII168[char][i],1)
	
def lcd_chinese_big(xPos, yPos, temp):
    	lcd_set_page(yPos,xPos)
   	for i in range(0, 24): 
		lcd_tranfer_data(Fonts.HZ[temp*72+i],1)
		
	lcd_set_page(yPos+1,xPos)
   	for i in range(24, 48): 
		lcd_tranfer_data(Fonts.HZ[temp*72+i],1)
		
	lcd_set_page(yPos+2,xPos)
   	for i in range(48, 72): 
		lcd_tranfer_data(Fonts.HZ[temp*72+i],1)

def lcd_init():
	GPIO.output(LCD_CS, True)
	GPIO.output(LCD_RST, False)		  	           
	GPIO.output(LCD_RST, True)
	lcd_tranfer_data(0xe2,0); 	#Internal reset
	
	lcd_tranfer_data(0xa3,0); 	#Sets the LCD drive voltage bias ratio
	##A2: 1/9 bias
	##A3: 1/7 bias (ST7565V)
	
	lcd_tranfer_data(0xa1,0);	#Sets the display RAM address SEG output correspondence
	##A0: normal
	##A1: reverse
	
	lcd_tranfer_data(0xc8,0); 	#Select COM output scan direction
	##C0~C7: normal direction
	##C8~CF: reverse direction
	
	lcd_tranfer_data(0xa4,0); 	#Display all points ON/OFF
	##A4: normal display
	##A5: all points ON
	
	lcd_tranfer_data(0xa6,0);	#Sets the LCD display normal/reverse
	##A6: normal
	##A7: reverse
	
	lcd_tranfer_data(0x2F,0);	#elect internal power supply operating mode
	##28~2F: Operating mode
	
	lcd_tranfer_data(0x40,0);	#Display start line set
	##40~7F Display start address
	
	lcd_tranfer_data(0x22,0); 	#V5 voltage regulator internal resistor ratio set(contrast)
	##20~27 small~large
	
	lcd_tranfer_data(0x81,0); 	#Electronic volume mode set
	##81: Set the V5 output voltage
	
	lcd_tranfer_data(0x34,0); 	#Electronic volume register set
	##00~3F: electronic volume register 
	
	lcd_tranfer_data(0xaf,0);   	#Display ON/OFF
	##AF: ON
	##AE: OFF
	lcd_clear()	                   

def lcd_clear():
	GPIO.output(LCD_CS, False)
	for i in range(0, 8):            
		lcd_set_page(i,0)
		for j in range(0, 128):          	                              
			lcd_tranfer_data(0x00,1)
	GPIO.output(LCD_CS, True)

def lcd_set_page(page, column):
	lsb = column & 0x0f
	msb = column & 0xf0
	msb = msb>>4
	msb = msb | 0x10                  
	page = page | 0xb0                               
	lcd_tranfer_data(page,0)
	lcd_tranfer_data(msb,0)
	lcd_tranfer_data(lsb,0)
	

def lcd_tranfer_data(value, SI):
	GPIO.output(LCD_CS, False)
	GPIO.output(LCD_CLK, True)
	if(SI):
		GPIO.output(LCD_A0, True)
	else:
		GPIO.output(LCD_A0, False)
	lcd_byte(value)
	GPIO.output(LCD_CS, True)


def lcd_byte(bits):
	tmp = bits;
	for i in range(0, 8): 
		GPIO.output(LCD_CLK, False)
		if(tmp & 0x80):
			GPIO.output(LCD_SI, True)
		else:
			GPIO.output(LCD_SI, False)
		tmp = (tmp<<1)
		GPIO.output(LCD_CLK, True)