#!/usr/bin/python
import subprocess
import pygame
import time
import sys
import re

HELP_MSG	= sys.argv[0]+" --address <IP> [--interval <X.Y>] [--max-ping <X>] [--history <X>] [--window-height <X>] [--window-width <X>] [--fullscreen] [--ping-threshold <X>]"

IP_ADDR		= "0.0.0.0" # Default IP
CLOCK_DELTA	= 0.1 # Minimal refresh rate
MAX_PING	= 500.0 # The visualization will automatically scale to display 0 ping on top and MAX_PING ping at the bottom
HISTORY_SIZE	= 600.0 # Number of history values to display
COORD_MULT	= {"X": 1, "Y": 1} # Coord scaler, automatically determined based on window size, MAX_PING and HISTORY_SIZE
RESOLUTION	= (640, 480) # Default window size
HISTORY		= []

TEXT_COLOR	= (180, 180, 180) # Infotext color

PING_THRESHOLD	= 250 # Ping above this value will raise the INTERNET DYING warning
LAG_THRESHOLD	= [ # You can define custom ping thresholds that will display lines across the screen
			{"ping": 60,  "color": (0, 160, 0), "desc": "Counter-Strike lag"},
			{"ping": 250, "color": (90, 90, 200), "desc": "Streaming lag"}
		]

def getNextArg():
	getNextArg.n = getNextArg.n + 1
	return sys.argv[getNextArg.n]
getNextArg.n = 0

def parseArgs():
	global HELP_MSG
	global IP_ADDR
	global MAX_PING
	global CLOCK_DELTA
	global HISTORY_SIZE
	global RESOLUTION
	global PING_THRESHOLD

	try:
		while (True):
			a = getNextArg()
			if   ((a == "--help") or (a == "-h")):
				print HELP_MSG
				exit()
			elif (a == "--address"):
				IP_ADDR = getNextArg()
			elif (a == "--max-ping"):
				MAX_PING = float(getNextArg())
			elif (a == "--interval"):
				CLOCK_DELTA = float(getNextArg())
			elif (a == "--history"):
				HISTORY_SIZE = float(getNextArg())
			elif (a == "--fullscreen"):
				RESOLUTION = (0, 0)
			elif (a == "--window-width"):
				RESOLUTION = (int(getNextArg()), RESOLUTION[1])
			elif (a == "--window-height"):
				RESOLUTION = (RESOLUTION[0], int(getNextArg()))
			elif (a == "--ping-threshold"):
				PING_THRESHOLD = float(getNextArg())
	except IndexError:
		pass

def normalizePoints(p):
	i = 0
	ret = []
	for point in p:
		ret.append((i*COORD_MULT["X"], point*COORD_MULT["Y"]))
		i = i+1
	return ret

def getPing(ip):
	try:
		r = subprocess.check_output("/bin/ping -qc 1 -W 1 "+ip, shell=True)
		rg = re.search("(\d+\.\d+)/\d+\.\d+/\d+\.\d+/\d+\.\d+", r)
		if (rg):
			return float(rg.group(1))
		else:
			return -1.0
	except:
		return -1.0

def main():
	global IP_ADDR
	global CLOCK_DELTA
	global HISTORY_SIZE
	global HISTORY
	global MAX_PING
	global RESOLUTION
	global COORD_MULT
	global HELP_MSG

	if (len(sys.argv) < 2):
		print HELP_MSG
		exit()

	parseArgs()

	CLOCK = -10.0

	pygame.init()
	pygame.display.set_caption("PingVis - "+IP_ADDR)
	if (RESOLUTION == (0, 0)):
		screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(RESOLUTION)
	font = pygame.font.SysFont("monospace", 15)

	screen.blit(font.render("LOADING", True, (255, 255, 255)), (10, 10))
	pygame.display.update()
	
	COORD_MULT["X"] = screen.get_width() / HISTORY_SIZE
	COORD_MULT["Y"] = screen.get_height() / MAX_PING

	while True:
		for e in pygame.event.get():
			if (e.type == pygame.QUIT):
				pygame.quit()
				exit()
			if (e.type == pygame.KEYDOWN):
				if ((e.key == 27) or (e.key == 113)):
					pygame.quit()
					exit()
		if (time.clock() > (CLOCK + CLOCK_DELTA)):
			CLOCK = time.clock()
			if (len(HISTORY) >= HISTORY_SIZE):
				HISTORY.pop(0)
			n = getPing(IP_ADDR)
			HISTORY.append(n)
			if (n > 100):
				print "=== INTERNET DYING ==="
			if (len(HISTORY) > 1):
				screen.fill((0, 0, 0))
				for l in LAG_THRESHOLD:
					pygame.draw.lines(screen, l["color"], False, [(0, l["ping"]*COORD_MULT["Y"]), (screen.get_width(), l["ping"]*COORD_MULT["Y"])], 1)
					screen.blit(font.render(l["desc"], 1, l["color"]), (5, l["ping"]*COORD_MULT["Y"]))

				screen.blit(font.render("Ping: "+str(HISTORY[len(HISTORY)-1])+"ms", 1, TEXT_COLOR), (5, screen.get_height()-20))
				if (HISTORY[len(HISTORY)-1] < 0):
					screen.blit(font.render("UNREACHABLE", 1, (255, 0, 0)), (120, screen.get_height()-20))
				screen.blit(font.render("MULT_X: "+str(COORD_MULT["X"])+", MULT_Y: "+str(COORD_MULT["Y"]), 1, TEXT_COLOR), (5, screen.get_height()-40))
				screen.blit(font.render("IP Address: "+IP_ADDR, 1, TEXT_COLOR), (5, screen.get_height()-60))
				screen.blit(font.render("Min interval: "+str(CLOCK_DELTA), 1, TEXT_COLOR), (5, screen.get_height()-80))
				screen.blit(font.render("Clock: "+str(CLOCK), 1, TEXT_COLOR), (5, screen.get_height()-100))
				screen.blit(font.render("Max ping: "+str(MAX_PING), 1, TEXT_COLOR), (5, screen.get_height()-120))
				screen.blit(font.render("History size: "+str(HISTORY_SIZE), 1, TEXT_COLOR), (5, screen.get_height()-140))
				
				pygame.draw.lines(screen, (255, 0, 0), False, normalizePoints(HISTORY), 1)
				pygame.display.update()

main()
