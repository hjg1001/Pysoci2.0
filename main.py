import pygame,setting,random,planet,key,game_ui
pygame.init()
font=pygame.font.Font('NotoSerifCJK-Regular.ttc',15)
font2=pygame.font.Font('NotoSerifCJK-Regular.ttc',40)
screen=pygame.display.set_mode(setting.screen_size)
clock=pygame.time.Clock()
class Map:
	def __init__(self):
		self.backup_surface,self.display_surface,self.s_map=pygame.Surface((setting.screen_size)),pygame.Surface((setting.screen_size)),pygame.Surface(setting.s_map_size)
		self.backup_surface.set_alpha(150)
		self.civ_list=[]
		self.vx,self.vy,self.m_u,self.m_d,self.m_r,self.m_l,self.m_s,self.m_check,self.pause,self.scale,self.m_x,self.planet_obj,self.m_id=0,0,False,False,False,False,False,False,False,1,False,None,0
		self.planet_sprite,self.ui_sprite=pygame.sprite.Group(),pygame.sprite.Group()
		self.m_planet=False#进入星球视图
		self.p_vx,self.p_vy=0,0
		self.info_list={}
		self.ui2_state,self.ui3_state,self.ui4_state=False,False,False
		self.ui4_list=[]
		while True:
			for _ in range(0,setting.planet[0]):
				xy=(random.randint(setting.planet[1],setting.map_size[0]-setting.planet[1]),random.randint(setting.planet[1],setting.map_size[1]-setting.planet[1]))
				if not self.planet_sprite or not any(pygame.Rect(xy[0]-setting.planet[1],xy[1]-setting.planet[1],2*setting.planet[1],2*setting.planet[1]).colliderect(pp.rect) for pp in self.planet_sprite):
					pp=planet.Planet(xy)
					self.planet_sprite.add(pp)
					if len(self.planet_sprite)==setting.planet[0]:break
			if len(self.planet_sprite)==setting.planet[0]:break
map=Map()
ui2,ui3,ui4=None,None,None
running=True
#调试
#map.planet_obj,map.m_planet=list(map.planet_sprite)[0],True
while running:
	clock.tick(setting.fps)
	fps=clock.get_fps()
	ui1=game_ui.ui1(fps,map)
	if map.ui2_state:ui2=game_ui.ui2(map)
	if map.ui3_state:ui3=game_ui.ui3(map)
	if map.ui4_state:ui4=game_ui.ui4(map)
	for event in pygame.event.get():
		key.control(event,map)
		ui1.event(event)
		if map.ui2_state and ui2:ui2.event(event)
		if map.ui3_state and ui3:ui3.event(event)
		if map.ui4_state and ui4:ui4.event(event)
		if event.type==pygame.QUIT:
			running=False
	key.act(map)
	screen.fill((0,0,0))
#----宇宙视图
	map.display_surface.fill((0,0,0))
	if not map.m_planet:
		#渲染星球
		map.planet_sprite.update(map,screen)
		if map.m_check:map.display_surface.blit(map.backup_surface,(0,0))
		#渲染显示图层
		screen.blit(map.display_surface,(map.vx,map.vy))
#----星球视图
	if map.m_planet:
		screen.blit(map.planet_obj.b_map,(map.p_vx,map.p_vy))
		map.planet_sprite.update(map,screen)
	#渲染小地图
	if setting.s_map:
		if not map.m_planet:
			map.s_map.fill((255,255,255))
			map.s_map.set_alpha(180)
			pygame.draw.rect(map.s_map,(0,0,0),((setting.s_map_size[0]/setting.map_size[0])*(-map.vx),(setting.s_map_size[1]/setting.map_size[1])*(-map.vy),(setting.s_map_size[0]/setting.map_size[0])*setting.screen_size[0],(setting.s_map_size[1]/setting.map_size[1])*setting.screen_size[1]),4)
			for p in map.planet_sprite:
				pygame.draw.circle(map.s_map,(0,0,0),((setting.s_map_size[0]/setting.map_size[0])*p.xy[0],(setting.s_map_size[1]/setting.map_size[1])*p.xy[1]),2)
			screen.blit(map.s_map,(0,setting.screen_size[1]-setting.s_map_size[1]-setting.s_map_y))
		else:
			map.s_map.fill((255,255,255))
			map.s_map.set_alpha(150)
			pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,setting.screen_size[1]-setting.s_map_size[1]-setting.s_map_y,setting.s_map_size[0],setting.s_map_size[1]),10)
			map.s_map.blit(pygame.transform.scale(map.planet_obj.map,setting.s_map_size),(0,0))
			pygame.draw.rect(map.s_map,(0,0,0),((setting.s_map_size[0]/(setting.planet_size*map.planet_obj.map_size[0]))*(-map.p_vx),(setting.s_map_size[1]/(setting.planet_size*map.planet_obj.map_size[1]))*(-map.p_vy),(setting.s_map_size[0]/(setting.planet_size*map.planet_obj.map_size[0]))*setting.screen_size[0],(setting.s_map_size[1]/(setting.planet_size*map.planet_obj.map_size[1])*setting.screen_size[1])),4)
			screen.blit(map.s_map,(0,setting.screen_size[1]-setting.s_map_size[1]-setting.s_map_y))
	#渲染左上角消息
	y=0
	if map.info_list:
		r_list=[]
		for info_list in map.info_list.items():
			if map.info_list[info_list[0]][0]:
				#(序列号,[信息,时间,surface])
				info_obj=info_list[1][2]
				if info_list[1][1]>0:
					if not map.pause:info_list[1][1]-=1
					text=font.render(info_list[1][0],True,(0,0,0),(255,255,5))
					screen.blit(text,(25,50+y*25))
					screen.blit(pygame.transform.scale(info_obj,(25,25)),(0,50+y*25))
				elif info_list[1][1]>-30:
					if not map.pause:info_list[1][1]-=1
					text=font.render(info_list[1][0],True,(0,0,0),(255,255,5))
					screen.blit(text,(25-abs(info_list[1][1]*((len(info_list[1][0])*15)/10)),50+y*25))
				else:r_list.append(info_list[0])
				y+=1
		for i in r_list:del map.info_list[i]
#---渲染UI
	if map.ui2_state and ui2:
		screen.blit(map.backup_surface,(0,0))
		ui2.draw(screen)
		pygame.draw.rect(screen,(255,255,255),ui2.rect,2)
		pygame.draw.line(screen,(255,255,250),(ui2.rect.x,ui2.rect.y+82),(ui2.rect.topright[0],ui2.rect.topright[1]+82))
	if map.ui3_state and ui3:
		screen.blit(map.backup_surface,(0,0))
		ui3.draw(screen)
		pygame.draw.rect(screen,(255,255,255),ui3.rect,2)
	if map.ui4_state and ui4:
		screen.blit(map.backup_surface,(0,0))
		ui4.draw(screen)
		pygame.draw.rect(screen,(255,255,255),ui4.rect,2)
	ui1.draw(screen)
	pygame.display.flip()
pygame.quit()