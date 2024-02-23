import pygame,setting,random
class Zx(pygame.sprite.Sprite):#准心
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((6,6))
		pygame.draw.circle(self.image,(55,255,25),(3,3),3)
		self.rect,self.x,self.y=self.image.get_rect(),setting.screen_size[0]//2,setting.screen_size[1]//2
		self.rect.topleft=(setting.screen_size[0]//2,setting.screen_size[1]//2)
	def update(self,screen,map):
		self.rect.topleft=(self.x-map.vx,self.y-map.vy)
		screen.blit(self.image,(self.x,self.y))
zx=Zx()
def control(event,map):
	if event.type==pygame.MOUSEBUTTONDOWN and not map.planet_obj and not map.ui2_state and not map.ui3_state and not map.ui4_state and not map.m_planet:
			zx.rect.topleft=event.pos
			p=pygame.sprite.spritecollide(zx,map.planet_sprite,False)
			if p:
				map.planet_obj=p[0]
				map.ui2_state=True
	if event.type == pygame.KEYDOWN:
		if event.key==pygame.K_UP:
				map.m_u=True
		if event.key==pygame.K_DOWN:
				map.m_d=True
		if event.key==pygame.K_LEFT:
				map.m_l=True
		if event.key==pygame.K_RIGHT:
				map.m_r=True
		if event.key==pygame.K_c and not map.pause:
			map.pause=True
		elif map.pause and event.key==pygame.K_c:
			map.pause=False
		#松开按键
	if event.type == pygame.KEYUP:
		if event.key==pygame.K_UP:
			map.m_u=False
		if event.key==pygame.K_DOWN:
			map.m_d=False
		if event.key==pygame.K_LEFT:
			map.m_l=False
		if event.key==pygame.K_RIGHT:
			map.m_r=False
def act(map):
	if not map.m_planet:
		if map.m_u and map.vy<30:
			map.vy+=10
		if map.m_d and -map.vy+setting.screen_size[1]<setting.map_size[1]+30:
			map.vy-=10
		if map.m_l and map.vx<30:
			map.vx+=10
		if map.m_r and -map.vx+setting.screen_size[0]<setting.map_size[0]+30:
			map.vx-=10
	else:#星球视图
		if map.m_u and map.p_vy<30:
			map.p_vy+=10
		if map.m_d and -map.p_vy+setting.screen_size[1]<map.planet_obj.map_size[1]*setting.planet_size+30:
			map.p_vy-=10
		if map.m_l and map.p_vx<30:
			map.p_vx+=10
		if map.m_r and -map.p_vx+setting.screen_size[0]<map.planet_obj.map_size[0]*setting.planet_size+30:
			map.p_vx-=10