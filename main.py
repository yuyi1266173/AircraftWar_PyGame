#!python3
#-*- codind: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import traceback
from myplane import MyPlane
from enemy import SmallEnemy, MidEnemy, BigEnemy

def add_enemies(group1, group2, type, num, bg_size):
	if type < 0 or type > 2:
		print("[add_enemies] type error! type = {}".format(type))
		raise TypeError("[add_enemies] type error! type = {}".format(type))

	while num:
		num -= 1
		if type == 0:
			enemy = SmallEnemy(bg_size)
		elif type == 1:
			enemy = MidEnemy(bg_size)
		else:
			enemy = BigEnemy(bg_size)
		
		group1.add(enemy)
		group2.add(enemy)


def main():
	pygame.mixer.pre_init()
	pygame.init()

	bg_size = width, height = 480, 700

	screen = pygame.display.set_mode(bg_size)
	pygame.display.set_caption("AircraftWar")
	pygame.key.set_repeat(100, 100)

	background = pygame.image.load('images/background.png').convert()

	pygame.mixer.music.load('sound/game_music.ogg')
	pygame.mixer.music.set_volume(0.2)

	enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
	enemy3_fly_sound.set_volume(0.2)

	clock = pygame.time.Clock()
	pygame.mixer.music.play()

	me = MyPlane(bg_size)
	
	enemies = pygame.sprite.Group()
	small_enemies = pygame.sprite.Group()
	mid_enemies = pygame.sprite.Group()
	big_enemies = pygame.sprite.Group()

	add_enemies(small_enemies, enemies, 0, 15, bg_size)
	add_enemies(mid_enemies, enemies, 1, 4, bg_size)
	add_enemies(big_enemies, enemies, 2, 2, bg_size)

	running = True
	switch_image = True
	delay = 5

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					me.moveLeft()
				elif event.key == K_RIGHT:
					me.moveRight()
				elif event.key == K_UP:
					me.moveUp()
				elif event.key == K_DOWN:
					me.moveDown()

		screen.blit( background, (0, 0) )

		delay -= 1
		
		if not delay:
			delay = 5
			switch_image = not switch_image
		
		for enemy in big_enemies:
			enemy.move()

			if switch_image:
				screen.blit(enemy.image1, enemy.rect)
			else:
				screen.blit(enemy.image2, enemy.rect)

			if enemy.rect.bottom > -50:
				enemy3_fly_sound.play()

		for enemy in mid_enemies:
			enemy.move()
			screen.blit(enemy.image, enemy.rect)

		for enemy in small_enemies:
			enemy.move()
			screen.blit(enemy.image, enemy.rect)

		if switch_image:
			screen.blit( me.image1, me.rect )
		else:
			screen.blit( me.image2, me.rect )
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