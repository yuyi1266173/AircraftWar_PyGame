#!python3
#-*- coding: utf-8 -*-

import pygame
from random import randint

class BulletSupply(pygame.sprite.Sprite):
	def __init__(self, bg_size):
		super(pygame.sprite.Sprite, self).__init__()
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/bullet_supply.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = bg_size
		self.rect.left = randint(0, self.width - self.rect.width)
		self.rect.bottom = -100
		self.speed = 5
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left = randint(0, self.width - self.rect.width)
		self.rect.bottom = -100



class BombSupply(pygame.sprite.Sprite):
	def __init__(self, bg_size):
		super(pygame.sprite.Sprite, self).__init__()
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/bomb_supply.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.width, self.height = bg_size
		self.rect.left = randint(0, self.width - self.rect.width)
		self.rect.bottom = -100
		self.speed = 5
		self.active = False
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.active = False

	def reset(self):
		self.active = True
		self.rect.left = randint(0, self.width - self.rect.width)
		self.rect.bottom = -100
