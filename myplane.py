#!python3
#-*- coding: utf-8 -*-

import pygame

class MyPlane(pygame.sprite.Sprite):
	def __init__(self, bg_size):
		super(pygame.sprite.Sprite, self).__init__()
		self.image1 = pygame.image.load('images/me1.png').convert_alpha()
		self.image2 = pygame.image.load('images/me2.png').convert_alpha()
		self.moveSpace = (bg_size[0], bg_size[1] - 60)
		self.rect = self.image1.get_rect()
		self.rect.left = (self.moveSpace[0] - self.rect.width) // 2
		self.rect.top = self.moveSpace[1] - self.rect.height
		self.speed = 10	
		self.active = True
		self.destroy_times = 0
		self.mask = pygame.mask.from_surface(self.image1)

		self.destroy_images = []
		self.destroy_images.extend( [\
			pygame.image.load('images/me_destroy_1.png').convert_alpha(),\
			pygame.image.load('images/me_destroy_2.png').convert_alpha(),\
			pygame.image.load('images/me_destroy_3.png').convert_alpha(),\
			pygame.image.load('images/me_destroy_4.png').convert_alpha(),\
			] )

	def moveUp(self):
		if self.rect.top > 0:
			self.rect.top -= self.speed
		else:
			self.rect.top = 0

	def moveDown(self):
		if self.rect.bottom < self.moveSpace[1]:
			self.rect.bottom += self.speed
		else:
			self.rect.bottom = self.moveSpace[1]

	def moveLeft(self):
		if self.rect.left > 0:
			self.rect.left -= self.speed
		else:
			self.rect.left = 0

	def moveRight(self):
		if self.rect.right < self.moveSpace[0]:
			self.rect.right += self.speed
		else:
			self.rect.right = self.moveSpace[0]

	def reset(self):
		self.rect.left = (self.moveSpace[0] - self.rect.width) // 2
		self.rect.top = self.moveSpace[1] - self.rect.height

	def destroy(self, screen):
		if not (self.destroy_times % 3):
			screen.blit( self.destroy_images[self.destroy_times//3], self.rect )

			if self.destroy_times == 9:
				self.reset()
				self.active = True
				self.destroy_times = 0

		if not self.active:
			self.destroy_times += 1



