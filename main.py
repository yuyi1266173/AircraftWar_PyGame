#!python3
#-*- codind: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import traceback
from myplane import MyPlane
from enemy import SmallEnemy, MidEnemy, BigEnemy
from bullet import Bullet1

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

	me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
	me_down_sound.set_volume(0.2)

	enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
	enemy1_down_sound.set_volume(0.2)

	enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
	enemy2_down_sound.set_volume(0.2)

	enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
	enemy3_fly_sound.set_volume(0.2)
	enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
	enemy3_fly_sound.set_volume(0.2)

	clock = pygame.time.Clock()
	pygame.mixer.music.play(-1)   #-1 cycle

	me = MyPlane(bg_size)
	
	enemies = pygame.sprite.Group()
	small_enemies = pygame.sprite.Group()
	mid_enemies = pygame.sprite.Group()
	big_enemies = pygame.sprite.Group()

	add_enemies(small_enemies, enemies, 0, 15, bg_size)
	add_enemies(mid_enemies, enemies, 1, 4, bg_size)
	add_enemies(big_enemies, enemies, 2, 2, bg_size)

	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4

	for i in range(BULLET1_NUM):
		bullet1.append( Bullet1(me.rect.midtop) ) 

	running = True
	switch_image = True
	delay = 10

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

		#enemies_down = pygame.sprite.spritecollide(me, enemies, False)
		enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)

		if enemies_down:
			me.active = False

			for e in enemies_down:
				e.active = False

		screen.blit( background, (0, 0) )

		delay -= 1
		
		if not (delay % 5):
			switch_image = not switch_image

			if not delay:
				delay = 10

				bullet1[bullet1_index].reset(me.rect.midtop)
				bullet1_index = (bullet1_index + 1) % BULLET1_NUM

		for b in bullet1:
			if b.active:
				b.move()
				screen.blit(b.image, b.rect)

				enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)

				if enemy_hit:
					b.active = False

					for e in enemy_hit:
						e.active = False
		
		for enemy in big_enemies:
			if enemy.active:
				enemy.move()

				if switch_image:
					screen.blit(enemy.image1, enemy.rect)
				else:
					screen.blit(enemy.image2, enemy.rect)

				if enemy.rect.bottom == -50:
					enemy3_fly_sound.play()
			else:
				enemy.destroy(screen, enemy3_down_sound)

		for enemy in mid_enemies:
			if enemy.active:
				enemy.move()
				screen.blit(enemy.image, enemy.rect)
			else:
				enemy.destroy(screen, enemy2_down_sound)

		for enemy in small_enemies:
			if enemy.active:
				enemy.move()
				screen.blit(enemy.image, enemy.rect)
			else:
				enemy.destroy(screen, enemy1_down_sound)

		if me.active:
			if switch_image:
				screen.blit( me.image1, me.rect )
			else:
				screen.blit( me.image2, me.rect )
		else:
			me.destroy(screen, me_down_sound)

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