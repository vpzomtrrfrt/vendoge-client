#!/usr/bin/env python3

#print("Loading...")

import ev3dev.ev3 as ev3
import ev3dev.fonts
import urllib.request
import time

m = ev3.LargeMotor("outA")
m2 = ev3.LargeMotor("outD")

scr = ev3.Screen()

HEADER_TEXT = "http://lonk.pw/k8"
AUTO_RES = None

if AUTO_RES != None:
	HEADER_TEXT = "DEBUG MODE"

header_font = ev3dev.fonts.load("lutBS14")

scr.draw.text((scr.xres/2-scr.draw.textsize(HEADER_TEXT, font=header_font)[0]/2, 1), HEADER_TEXT, font=header_font)
scr.update()

code = ""
code_font = ev3dev.fonts.load('ncenB24')

def draw_code():
	scr.draw.rectangle([(2,40), (scr.xres-2,70)], "white")
	if len(code) > 0:
		scr.draw.rectangle(((2,70), (scr.xres-2,90)), "white")
		scr.draw.text((scr.xres/2-scr.draw.textsize(code, font=code_font)[0]/2,40), code, font=code_font)
	scr.update()

def on_backspace(thing, state):
	global code
	if state:
		if len(code) < 1:
			exit()
			return
		code = code[:-1]
		draw_code()

def parseRes(res):
	spl = res.decode('utf-8').strip().split(",")
	count1 = int(spl[0])
	count2 = int(spl[1])
	return (count1, count2)

def on_enter(thing, state):
	global code
	if state:
		realCode = code
		code = "Checking..."
		draw_code()
		res = None
		count1 = 0
		count2 = 0
		if AUTO_RES == None:
			try:
				h = urllib.request.urlopen("https://polar-shore-34463.herokuapp.com/redeem/"+realCode)
				res = h.read()
				h.close()
				count1, count2 = parseRes(res)
			except urllib.error.HTTPError as e:
				res = e.read()
		else:
			res = AUTO_RES
			count1, count2 = parseRes(res)
		scr.draw.text((2,70), res)
		if count1 > 0:
			m.run_to_rel_pos(speed_sp=800, position_sp=m.count_per_rot*count1, stop_action="hold")
		for i in range(0, count2):
			m2.run_to_abs_pos(speed_sp=300, position_sp=-m2.count_per_rot/24, stop_action="coast")
			m2.wait_while(m2.STATE_RUNNING)
			m2.run_to_abs_pos(speed_sp=500, position_sp=0, stop_action="hold")
			m2.wait_while(m2.STATE_RUNNING, 2000)
			time.sleep(0.5)
		code = ""
		draw_code()

def code_char(char):
	def tr(self, state):
		global code
		if state:
			code += char
			draw_code()
	return tr

ev3.Button.on_up = code_char("0")
ev3.Button.on_right = code_char("1")
ev3.Button.on_down = code_char("2")
ev3.Button.on_left = code_char("3")
ev3.Button.on_backspace = on_backspace
ev3.Button.on_enter = on_enter

btn = ev3.Button()
while True:
	btn.process()
