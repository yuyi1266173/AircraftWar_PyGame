#!python3
#-*- codind: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit

def main():
	pygame.mixer.pre_init()
	pygame.init()

	bg_size = width, height = 480, 700

	screen = pygame.display.set_mode(bg_size)
	pygame.display.set_caption("AircraftWar")

	clock = pygame.time.Clock()

	running = True

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		screen.fill( (255, 255, 255) )
		clock.tick(60)

		#pygame.display.flip()
		pygame.display.update()


if __name__ == "__main__":
	try:
		main()
	except SystemExit:
		pass
	except:
		pygame.quit()