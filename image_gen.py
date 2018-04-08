from tkinter import *
import random as rand
from datetime import datetime
import pyautogui as auto
from threading import Thread
from time import sleep
import sys
from twitter_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from twython import Twython

def draw_rand_oval():
	color = get_rand_color()
	border = get_rand_color()
	dist = rand.randrange(MAX)
	x0 = rand.randrange(MAX)
	y0 = rand.randrange(MAX)
	x1 = rand.randrange(MAX)
	y1 = rand.randrange(MAX)
	canvas.create_oval(x0, y0, x1, y1, fill=color, outline=border)

def draw_rand_arc():
	color = get_rand_color()
	border = get_rand_color()
	dist = rand.randrange(MAX)
	x0 = rand.randrange(MAX)
	y0 = rand.randrange(MAX)
	x1 = rand.randrange(MAX)
	y1 = rand.randrange(MAX)
	canvas.create_arc(x0, y0, x1, y1, fill=color, outline=border, stipple='gray12', style='chord')	

def draw_rand_line():
	color = get_rand_color()
	width = rand.randrange(7)
	x0 = rand.randrange(MAX)
	x1 = rand.randrange(MAX)
	y0 = rand.randrange(MAX)
	y1 = rand.randrange(MAX)
	canvas.create_line(x0, x1, y0, y1, fill=color, width=width)

def get_rand_color():
	# Generate a random 8 bit color hex string based on hour of day
	'''
	morning = 6-9 (4)	dark colors
	day 	= 10-17 (8)	normal colors
	evening = 18-21 (4)	dark colors
	night 	= 22-5 (8)	b & w
	'''
	hour = int(cur_hour)
	if((hour >= 6  and hour <= 9) or (hour >=18 and hour <= 21)):
		return get_rand_color_dark()
	if(hour >= 22 or hour <= 5):
		return get_rand_color_bw()
	hex_str = '#'	
	for i in range(HEX_LEN):
		digit = get_hex_digit(rand.randrange(HEX_MAX + 1))
		hex_str += str(digit)
	return hex_str

def get_rand_color_dark():
	# Generate a random 8 bit color hex string
	hex_str = '#'
	for i in range(HEX_LEN):
		if(i == 0 or i % 2 == 0):
			hex_str += str(rand.randrange(8))
		else:
			digit = get_hex_digit(rand.randrange(HEX_MAX + 1))
			hex_str += str(digit)
	return hex_str

def get_rand_color_bw():
	hex_str = '#'
	value1 = get_hex_digit(rand.randrange(HEX_MAX + 1))
	value2 = get_hex_digit(rand.randrange(HEX_MAX + 1))
	for i in range(int(HEX_LEN / 2)):
		hex_str += str(value1)
		hex_str += str(value2)
	return hex_str

def get_hex_digit(num):
	if(num < 0):
		return 0
	if(num > 15):
		return 15
	if(num < 10):
		return num
	return {
		10:'a',
		11:'b',
		12:'c',
		13:'d',
		14:'e',
		15:'f'
	}[num]

def draw_rand_polygon():
	color = get_rand_color()
	border = get_rand_color()
	num_vertices = rand.randrange(2, 50)
	vertices = []
	for i in range(num_vertices):
		vertices.append(get_rand_vertice())
	canvas.create_polygon(*vertices, fill=color, stipple='gray12', outline=border)

def draw_rand_rectangle():
	color = get_rand_color()
	border = get_rand_color()
	vertices = []
	vertices.append(get_rand_vertice())
	vertices.append(get_rand_vertice())
	canvas.create_rectangle(*vertices, fill=color, stipple='gray12', outline=border)

def get_rand_vertice():
	return (rand.randrange(MAX * -1.1, MAX * 1.1),
	rand.randrange(MAX * -1.05, MAX * 1.05))

def fill_canvas():
	num_repeats = rand.randrange(1000)
	for i in range(rand.randrange(num_repeats)):
		choice = rand.randrange(5)
		if(choice == 0):
			draw_rand_oval()
		elif(choice == 1):
			draw_rand_line()	
		elif(choice == 2):
			draw_rand_rectangle()
		elif(choice ==3):
			draw_rand_arc()
		else:
			draw_rand_polygon()

class ScreenshotThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.daemon = True
	
	def run(self):
		sleep(5)
		print("Taking screenshot")
		x = canvas.winfo_rootx() + 50
		y = canvas.winfo_rooty() + 50
		img = auto.screenshot(region=(x, y, MAX-x,  MAX-y))
		img.save(image_file_name)
		sleep(5)
		root.destroy()

cur_hour = datetime.now().strftime('%H')
image_file_name = 'art.jpg'
MAX = 600
HEX_MAX = 15
HEX_LEN = 6

root = Tk()
root.geometry("%dx%d+%d+%d" % (MAX, MAX, 50, 50))
canvas = Canvas(root, width=MAX, height=MAX, bg='black')
canvas.pack()
print('Creating artwork')
fill_canvas()

scrn = ScreenshotThread()
scrn.start()
mainloop()

print('Updating Twitter status with image')
twtr = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET) 
img_bytes = open(image_file_name, 'rb')
response = twtr.upload_media(media=img_bytes)
twtr.update_status(media_ids=[response['media_id']])
