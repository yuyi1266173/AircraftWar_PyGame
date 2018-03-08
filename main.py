#!python3
#-*- codind: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import traceback

def main():
	pygame.mixer.pre_init()
	pygame.init()

	bg_size = width, height = 480, 700

	screen = pygame.display.set_mode(bg_size)
	pygame.display.set_caption("AircraftWar")

	background = pygame.image.load('images/background.png').convert()

	pygame.mixer.music.load('sound/game_music.ogg')
	pygame.mixer.music.set_volume(0.2)

	clock = pygame.time.Clock()
	pygame.mixer.music.play()

	running = True

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		screen.blit( background,(0, 0) )
		clock.tick(60)

		#pygame.display.flip()
		pygame.display.update()


if __name__ == "__main__":
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		#input()