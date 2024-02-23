import pygame,tile,random
class water(pygame.sprite.Sprite):
	def __init__(self,surface,xy):
		pygame.sprite.Sprite.__init__(self)
		self.image=surface
		self.rect=self.image.get_rect()
		self.rect.topleft=xy