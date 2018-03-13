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

	score = 0
	score_font = pygame.font.Font('font/font.TTF', 36)

	paused = False
	pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
	pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
	resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
	resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
	paused_rect = pause_nor_image.get_rect()
	paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
	paused_image = pause_nor_image 

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			elif event.type == KEYDOWN:
				if not paused:
					if event.key == K_LEFT:
						me.moveLeft()
					elif event.key == K_RIGHT:
						me.moveRight()
					elif event.key == K_UP:
						me.moveUp()
					elif event.key == K_DOWN:
						me.moveDown()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused

					if paused:
						paused_image = resume_pressed_image
						pygame.mixer.music.pause()
					else:
						paused_image = pause_pressed_image
						pygame.mixer.music.unpause()

			elif event.type == MOUSEMOTION:
				if paused_rect.collidepoint(event.pos):
					if paused:
						paused_image = resume_pressed_image
					else:
						paused_image = pause_pressed_image
				else:
					if paused:
						paused_image = resume_nor_image
					else:
						paused_image = pause_nor_image

		screen.blit( background, (0, 0) )

		if not paused:
			#enemies_down = pygame.sprite.spritecollide(me, enemies, False)
			enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)

			if enemies_down:
				me.active = False

				for e in enemies_down:
					e.active = False

			delay -= 1
			
			if not (delay % 5):
				switch_image = not switch_image

				if not delay:
					delay = 10

					bullet1[bullet1_index].reset(me.rect.midtop)
					bullet1_index = (bullet1_index + 1) % BULLET1_NUM

		if paused:
			switch_image = False

		for b in bullet1:
			if b.active:
				if not paused:
					b.move()

				screen.blit(b.image, b.rect)

				if not paused:
					enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)

					if enemy_hit:
						b.active = False

						for e in enemy_hit:
							if e in mid_enemies or e in big_enemies:
								e.energy -= 1
								e.hit = True

								if not e.energy:
									e.active = False
							else:
								e.active = False
		
		for enemy in big_enemies:
			if enemy.active:
				if not paused:
					enemy.move()

				if enemy.hit:
					screen.blit(enemy.image_hit, enemy.rect)
					enemy.hit = False
				else:
					if switch_image:
						screen.blit(enemy.image1, enemy.rect)
					else:
						screen.blit(enemy.image2, enemy.rect)

				pygame.draw.line(screen, (0, 0, 0),\
				 (enemy.rect.left, enemy.rect.top-5), (enemy.rect.right, enemy.rect.top-5), 2)
				energy_remain = enemy.energy / BigEnemy.energy
				if energy_remain > 0.2:
					energy_color = (0, 255, 0)
				else:
					energy_color = (255, 0, 0)

				pygame.draw.line(screen, energy_color, (enemy.rect.left, enemy.rect.top-5),\
				    (enemy.rect.left+energy_remain*enemy.rect.width, enemy.rect.top-5), 2)

				if enemy.rect.bottom == -50:
					enemy3_fly_sound.play()
			else:
				if enemy.destroy(screen, enemy3_down_sound):
					score += 10000

		for enemy in mid_enemies:
			if enemy.active:
				if not paused:
					enemy.move()

				if enemy.hit:
					screen.blit(enemy.image_hit, enemy.rect)
					enemy.hit = False
				else:
					screen.blit(enemy.image, enemy.rect)

				pygame.draw.line(screen, (0, 0, 0),\
				 (enemy.rect.left, enemy.rect.top-5), (enemy.rect.right, enemy.rect.top-5), 2)
				energy_remain = enemy.energy / MidEnemy.energy
				if energy_remain > 0.2:
					energy_color = (0, 255, 0)
				else:
					energy_color = (255, 0, 0)
				pygame.draw.line(screen, energy_color, (enemy.rect.left, enemy.rect.top-5),\
				    (enemy.rect.left+energy_remain*enemy.rect.width, enemy.rect.top-5), 2)
			else:
				if enemy.destroy(screen, enemy2_down_sound):
					score += 5000

		for enemy in small_enemies:
			if enemy.active:
				if not paused:
					enemy.move()
				screen.blit(enemy.image, enemy.rect)
			else:
				if enemy.destroy(screen, enemy1_down_sound):
					score += 1000

		if me.active:
			if switch_image:
				screen.blit( me.image1, me.rect )
			else:
				screen.blit( me.image2, me.rect )
		else:
			me.destroy(screen, me_down_sound)

		score_text = score_font.render("Score : %s" % str(score), True, (255, 255, 255) )
		screen.blit(score_text, (10, 5))

		screen.blit(paused_image, paused_rect)

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