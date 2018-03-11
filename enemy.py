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
		self.rect.bottom = randint(-5*self.rect.height, 0)
		self.speed = 2

	def reset(self):
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-5*self.rect.height, 0)

	def move(self):
		if self.rect.top < self.moveSpace[1]:
			self.rect.top += self.speed
		else:
			self.reset()


class MidEnemy(pygame.sprite.Sprite):
	def __init__(self,  bg_size):
		#super(pygame.sprite.Sprite, self).__init__()
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/enemy2.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.moveSpace = bg_size
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-10*self.rect.height, 0)
		self.speed = 1

	def reset(self):
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-10*self.rect.height, 0)

	def move(self):
		if self.rect.top < self.moveSpace[1]:
			self.rect.top += self.speed
		else:
			self.reset()


class BigEnemy(pygame.sprite.Sprite):
	def __init__(self,  bg_size):
		#super(pygame.sprite.Sprite, self).__init__()
		pygame.sprite.Sprite.__init__(self)

		self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
		self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
		self.rect = self.image1.get_rect()
		self.moveSpace = bg_size
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-15*self.rect.height, 0)
		self.speed = 1

	def reset(self):
		self.rect.left = randint(0, self.moveSpace[0] - self.rect.width)
		self.rect.bottom = randint(-15*self.rect.height, 0)

	def move(self):
		if self.rect.top < self.moveSpace[1]:
			self.rect.top += self.speed
		else:
			self.reset()

