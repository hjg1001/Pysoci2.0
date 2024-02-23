import pygame,tile
pygame.init()
screen=pygame.display.set_mode((40,30))
def gun_img(flag,id):
	a=pygame.transform.scale(flag,(40,15)).convert_alpha()
	a.blit(tile.gun[id],(0,0))
	for x in range(40):
		for y in range(15):
			if a.get_at((x,y))==(11,255,45):a.set_at((x,y),(11,255,45,0))
	return a
class Gun:
	def __init__(self,name,flag,reload_time,ammo,z,damage,id,s,n,cost):
		self.name=name
		self.damage=damage
		self.z=z#命中率(初始)
		self.ammo=[0,ammo]
		self.s_time=[0,s]#射速
		self.reload=[0,reload_time]
		self.image=gun_img(flag,id)
		self.n=n#耐久
		self.cost=cost
	def fire(self):
		pass
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y,owner):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Rect(x,y,1,1)
		self.owner=owner