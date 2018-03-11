#!python3
#-*- coding: utf-8 -*-

import pygame
from random import randint


class SmallEnemy(pygame.sprite.Sprite):
	def __init__(self,  bg_size):
		#super(pygame.sprite.Sprite, self).__init__()
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/enemy1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.moveSpace = bg_size
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-5*self.moveSpace[1], 0)
		self.speed = 2
		self.active = True
		self.destroy_times = 0
		self.mask = pygame.mask.from_surface(self.image)

		self.destroy_images = []
		self.destroy_images.extend( [\
			pygame.image.load('images/enemy1_down1.png').convert_alpha(),\
			pygame.image.load('images/enemy1_down2.png').convert_alpha(),\
			pygame.image.load('images/enemy1_down3.png').convert_alpha(),\
			pygame.image.load('images/enemy1_down4.png').convert_alpha(),\
			] )

	def reset(self):
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-5*self.moveSpace[1], 0)

	def move(self):
		if self.rect.top < self.moveSpace[1]:
			self.rect.top += self.speed
		else:
			self.reset()

	def destroy(self, screen, destroy_sound):
		add_score_flag = False

		if not self.destroy_times:
			destroy_sound.play()
			add_score_flag = True

		if not (self.destroy_times % 3):
			screen.blit( self.destroy_images[self.destroy_times//3], self.rect )

			if self.destroy_times == 9:
				self.reset()
				self.active = True
				self.destroy_times = 0

		if not self.active:
			self.destroy_times += 1

		return add_score_flag


class MidEnemy(pygame.sprite.Sprite):
	energy = 8

	def __init__(self,  bg_size):
		#super(pygame.sprite.Sprite, self).__init__()
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/enemy2.png').convert_alpha()
		self.image_hit = pygame.image.load('images/enemy2_hit.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.moveSpace = bg_size
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-10*self.moveSpace[1], -self.moveSpace[1])
		self.speed = 1
		self.active = True
		self.destroy_times = 0
		self.mask = pygame.mask.from_surface(self.image)
		self.energy = MidEnemy.energy
		self.hit = False

		self.destroy_images = []
		self.destroy_images.extend( [\
			pygame.image.load('images/enemy2_down1.png').convert_alpha(),\
			pygame.image.load('images/enemy2_down2.png').convert_alpha(),\
			pygame.image.load('images/enemy2_down3.png').convert_alpha(),\
			pygame.image.load('images/enemy2_down4.png').convert_alpha(),\
			] )

	def reset(self):
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-10*self.moveSpace[1], -self.moveSpace[1])
		self.active = True
		self.destroy_times = 0
		self.energy = MidEnemy.energy

	def move(self):
		if self.rect.top < self.moveSpace[1]:
			self.rect.top += self.speed
		else:
			self.reset()

	def destroy(self, screen, destroy_sound):
		add_score_flag = False

		if not self.destroy_times:
			destroy_sound.play()
			add_score_flag = True

		if not (self.destroy_times % 3):
			screen.blit( self.destroy_images[self.destroy_times//3], self.rect )

			if self.destroy_times == 9:
				self.reset()

		if not self.active:
			self.destroy_times += 1

		return add_score_flag


class BigEnemy(pygame.sprite.Sprite):
	energy = 20

	def __init__(self,  bg_size):
		#super(pygame.sprite.Sprite, self).__init__()
		pygame.sprite.Sprite.__init__(self)

		self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
		self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
		self.image_hit = pygame.image.load('images/enemy3_hit.png').convert_alpha()
		self.rect = self.image1.get_rect()
		self.moveSpace = bg_size
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-15*self.moveSpace[1], -5 * self.moveSpace[1])
		self.speed = 1
		self.active = True
		self.destroy_times = 0
		self.mask = pygame.mask.from_surface(self.image1)
		self.energy = BigEnemy.energy
		self.hit = False

		self.destroy_images = []
		self.destroy_images.extend( [\
			pygame.image.load('images/enemy3_down1.png').convert_alpha(),\
			pygame.image.load('images/enemy3_down2.png').convert_alpha(),\
			pygame.image.load('images/enemy3_down3.png').convert_alpha(),\
			pygame.image.load('images/enemy3_down4.png').convert_alpha(),\
			pygame.image.load('images/enemy3_down5.png').convert_alpha(),\
			pygame.image.load('images/enemy3_down6.png').convert_alpha(),\
			] )

	def reset(self):
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-15*self.moveSpace[1], -5 * self.moveSpace[1])
		self.active = True
		self.destroy_times = 0
		self.energy = BigEnemy.energy

	def move(self):
		if self.rect.top < self.moveSpace[1]:
			self.rect.top += self.speed
		else:
			self.reset()

	def destroy(self, screen, destroy_sound):
		add_score_flag = False

		if not self.destroy_times:
			destroy_sound.play()
			add_score_flag = True

		if not (self.destroy_times % 3):
			screen.blit( self.destroy_images[self.destroy_times//3], self.rect )

			if self.destroy_times == 15:
				self.reset()

		if not self.active:
			self.destroy_times += 1

		return add_score_flag

