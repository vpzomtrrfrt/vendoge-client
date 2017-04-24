#!/usr/bin/env python3

#print("Loading...")

import ev3dev.ev3 as ev3
import ev3dev.fonts
import urllib.request

m = ev3.LargeMotor("outA")

scr = ev3.Screen()

HEADER_TEXT = "http://lonk.pw/k8"

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

def on_enter(thing, state):
	global code
	if state:
		realCode = code
		code = "Checking..."
		draw_code()
		res = None
		count = 0
		try:
			h = urllib.request.urlopen("https://polar-shore-34463.herokuapp.com/redeem/"+realCode)
			res = h.read()
			h.close()
			count = float(res.strip())
		except urllib.error.HTTPError as e:
			res = e.read()
			success = False
		if count > 0:
			m.run_to_rel_pos(speed_sp=800, position_sp=m.count_per_rot*count, stop_action="hold")
		scr.draw.text((2,70), res)
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
