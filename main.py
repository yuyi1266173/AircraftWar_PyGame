#!python3
#-*- codind: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import traceback
import random

from myplane import MyPlane
from enemy import SmallEnemy, MidEnemy, BigEnemy
from bullet import Bullet1, Bullet2
from supply import BulletSupply, BombSupply

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


def inc_speed(target, inc):
	for each in target:
		each.speed += inc


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

	life_image = pygame.image.load('images/life.png').convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3

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

	upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
	upgrade_sound.set_volume(0.2)

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

	bullets = []
	bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
	bullet_sound.set_volume(0.2)

	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4

	for i in range(BULLET1_NUM):
		bullet1.append( Bullet1(me.rect.midtop) ) 

	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 8

	for i in range(BULLET2_NUM //2):
		bullet2.append( Bullet2( (me.rect.centerx - 33, me.rect.centery) ) )
		bullet2.append( Bullet2( (me.rect.centerx + 30, me.rect.centery) ) )

	DOUBLE_BULLET_TIME = USEREVENT + 1
	is_double_bullet = False


	running = True
	switch_image = True
	delay = 10

	score = 0
	score_font = pygame.font.Font('font/font.TTF', 36)

	level = 1
	level_change_flag = 0

	paused = False
	pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
	pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
	resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
	resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
	paused_rect = pause_nor_image.get_rect()
	paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
	paused_image = pause_nor_image 

	bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
	bomb_sound.set_volume(0.2)
	bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font('font/font.ttf', 48)
	bomb_num = 3

	supply_sound = pygame.mixer.Sound('sound/supply.wav')
	supply_sound.set_volume(0.2)
	get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
	get_bomb_sound.set_volume(0.2)
	get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
	get_bullet_sound.set_volume(0.2)
	bomb_supply = BombSupply(bg_size)
	bullet_supply = BulletSupply(bg_size)
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

	INVINCIBLE_TIME = USEREVENT + 2

	recorded = False
	record_score = 0
	gameover_font = pygame.font.Font('font/Font.ttf', 48)
	gameover_image = pygame.image.load('images/gameover.png').convert_alpha()
	gameover_rect = gameover_image.get_rect()
	again_image = pygame.image.load('images/again.png').convert_alpha()
	again_rect = again_image.get_rect()

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
					elif event.key == K_SPACE:
						if bomb_num:
							bomb_num -= 1
							bomb_sound.play()

							for each in enemies:
								if each.rect.bottom > 0:
									each.active = False

			elif event.type == SUPPLY_TIME:
				if not paused:
					supply_sound.play()

					if random.choice( [True, False] ):
						bomb_supply.reset()
					else:
						bullet_supply.reset()

			elif event.type == DOUBLE_BULLET_TIME:
				is_double_bullet = False
				pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

			elif event.type == INVINCIBLE_TIME:
				me.invincible = False
				pygame.time.set_timer(INVINCIBLE_TIME, 0)

			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused

					if paused:
						paused_image = resume_pressed_image
						pygame.mixer.music.pause()
						pygame.mixer.pause()
						pygame.time.set_timer(SUPPLY_TIME, 0)
						pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
					else:
						paused_image = pause_pressed_image
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()
						pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
						pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)

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

			if enemies_down and not me.invincible:
				me.active = False

				for e in enemies_down:
					e.active = False

			delay -= 1
			
			if not (delay % 5):
				switch_image = not switch_image

				if not delay:
					delay = 10
					bullet_sound.play()

					if is_double_bullet:
						bullets = bullet2
						bullet2[bullet2_index].reset( (me.rect.centerx - 33, me.rect.centery) )
						bullet2[bullet2_index + 1].reset( (me.rect.centerx + 30, me.rect.centery) )
						bullet2_index = (bullet2_index + 2) % BULLET2_NUM
					else:
						bullets = bullet1
						bullet1[bullet1_index].reset(me.rect.midtop)
						bullet1_index = (bullet1_index + 1) % BULLET1_NUM

		if paused:
			switch_image = False

		for b in bullets:
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
			if me.destroy(screen, me_down_sound):
				life_num -= 1
				pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

		if bomb_supply.active:
			if not paused:
				bomb_supply.move()

				if pygame.sprite.collide_mask(bomb_supply, me):
					get_bomb_sound.play()
					bomb_supply.active = False

					if bomb_num < 3:
						bomb_num += 1

			screen.blit(bomb_supply.image, bomb_supply.rect)

		if bullet_supply.active:
			if not paused:
				bullet_supply.move()

				if pygame.sprite.collide_mask(bullet_supply, me):
					get_bullet_sound.play()
					bullet_supply.active = False
					is_double_bullet = True
					pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)

			screen.blit(bullet_supply.image, bullet_supply.rect)


		if level == 1 and score > 50000:
			level = 2
			level_change_flag = 1
			upgrade_sound.play()
			add_enemies(small_enemies, enemies, 0, 3, bg_size)
			add_enemies(mid_enemies, enemies, 1, 2, bg_size)
			add_enemies(big_enemies, enemies, 2, 1, bg_size)
			inc_speed(small_enemies, 1)
		elif level == 2 and score > 300000:
			level = 3
			level_change_flag = 1
			upgrade_sound.play()
			add_enemies(small_enemies, enemies, 0, 5, bg_size)
			add_enemies(mid_enemies, enemies, 1, 3, bg_size)
			add_enemies(big_enemies, enemies, 2, 2, bg_size)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)
		elif level == 3 and score > 600000:
			level = 4
			level_change_flag = 1
			upgrade_sound.play()
			add_enemies(small_enemies, enemies, 0, 5, bg_size)
			add_enemies(mid_enemies, enemies, 1, 3, bg_size)
			add_enemies(big_enemies, enemies, 2, 2, bg_size)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)
		elif level == 4 and score > 1000000:
			level = 5
			level_change_flag = 1
			upgrade_sound.play()
			add_enemies(small_enemies, enemies, 0, 5, bg_size)
			add_enemies(mid_enemies, enemies, 1, 3, bg_size)
			add_enemies(big_enemies, enemies, 2, 2, bg_size)
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		if level_change_flag > 0:
			level_change_flag += 1
			level_text = score_font.render("Level : %d" % level, True, (255, 0, 0) )
			level_text_rect = level_text.get_rect()
			screen.blit(level_text, ( (width-level_text_rect.width)//2, (height-level_text_rect.height)//2 ) )

			if level_change_flag == 100:
				level_change_flag = 0

		score_text = score_font.render("Score : %s" % str(score), True, (255, 255, 255) )
		screen.blit(score_text, (10, 5))

		bomb_text = bomb_font.render("x %d" % bomb_num, True, (255, 255, 255) )
		text_rect = bomb_text.get_rect()
		screen.blit(bomb_image, (10, height - 10 - bomb_rect.height) )
		screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height) )

		screen.blit(paused_image, paused_rect)

		if life_num:
			for i in range(life_num):
				screen.blit(life_image, (width-10-(i+1)*life_rect.width, height-10-life_rect.height) )
		else:
			#print("Game Over!!!")
			pygame.mixer.music.stop()
			pygame.mixer.stop()
			paused = True

			pygame.time.set_timer(SUPPLY_TIME, 0);

			if not recorded:
				recorded = True

				try:
					with open('record.txt', 'r') as f:
						temp = f.read()
						print(temp)
						if temp:
							record_score = int(temp)
				except FileNotFoundError:
					record_score = 0

				if score > record_score:
					with open('record.txt', 'w') as f:
						f.write(str(score))

			record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255) )
			screen.blit(record_score_text, (20, 50) )

			gameover_text1 = gameover_font.render("Your Socre", True, (255, 255, 255) )
			gameover_text1_rect = gameover_text1.get_rect()
			gameover_text1_rect.left = (width - gameover_text1_rect.width) // 2
			gameover_text1_rect.top = height // 3
			screen.blit(gameover_text1, gameover_text1_rect)

			gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
			gameover_text2_rect = gameover_text2.get_rect()
			gameover_text2_rect.left = (width - gameover_text2_rect.width) // 2
			gameover_text2_rect.top = gameover_text1_rect.bottom + 10
			screen.blit(gameover_text2, gameover_text2_rect)

			again_rect.left = (width - again_rect.width) // 2
			again_rect.top = gameover_text2_rect.bottom + 50
			screen.blit(again_image, again_rect)

			gameover_rect.left = (width - again_rect.width) // 2
			gameover_rect.top = again_rect.bottom + 10
			screen.blit(gameover_image, gameover_rect)

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()

				if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
					main()
				elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
					pygame.quit()
					exit()

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