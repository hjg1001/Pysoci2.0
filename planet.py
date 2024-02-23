import pygame,setting,random,text,os,terrain,bio,function
class Planet(pygame.sprite.Sprite):
	def __init__(self,xy):
		pygame.sprite.Sprite.__init__(self)
		self.mass,self.xy,self.color=random.randint(setting.planet[2][0],setting.planet[2][1]),xy,(random.randint(50,255),random.randint(50,255),random.randint(50,255))
		self.map_size=(int(50*self.mass),int(50*self.mass))
		self.image=pygame.Surface((self.mass*2*setting.debug,self.mass*2*setting.debug))
		pygame.draw.circle(self.image,self.color,(self.mass*setting.debug,self.mass*setting.debug),self.mass*setting.debug)
		self.rect=self.image.get_rect()
		self.rect.topleft=xy
		self.type='星球'
		self.O_list={}#组织列表
		self.name=''
		self.rs_group=pygame.sprite.Group()
		self.map,self.area_group,self.bio_group,self.resource_group,self.fm_group,self.building_group=pygame.Surface(self.map_size),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()
		folders = [f for f in os.listdir('map/map_list') ]
		fd=f'map/map_list/{random.choice(folders)}'
		self.map.fill((57,87,28))
		self.dis=False#是否渲染精灵
		self.b_map=pygame.transform.scale(self.map,(self.map_size[0]*setting.planet_size,self.map_size[1]*setting.planet_size))
		#放置水域
		for f in os.listdir(fd):
			if f[:len(f)-4]!='map' and f[len(f)-3:len(f)]=='png':
				img=pygame.image.load(fd+'/'+f)
				w=terrain.water(pygame.transform.scale(img,(img.get_width()*self.mass*setting.planet_size,img.get_height()*setting.planet_size*self.mass)),(eval(f[:len(f)-4])[0]*setting.planet_size*self.mass,eval(f[:len(f)-4])[1]*setting.planet_size*self.mass))
				self.area_group.add(w)
		self.area_group.draw(self.b_map)
		self.map=pygame.transform.scale(self.b_map,(self.map_size))
		if setting.civ[0]>setting.civ_num:#放置文明
			setting.civ_num+=1
			while True:
				xy=(random.randint(0,self.map_size[0]),random.randint(0,self.map_size[1]))
				if not pygame.sprite.spritecollide(function.Rect((10,25),xy),self.area_group,False,pygame.sprite.collide_mask):
					hm=bio.human(xy,self)
					hm.age=18
					self.bio_group.add(hm)
				if len(self.bio_group)==setting.civ[1]:break
		for _ in range(0,random.randint(setting.planet[3][0],setting.planet[3][1])):
			self.name+=random.choice(text.planet_name)
	def update(self,map,screen):
		for o in self.O_list:self.O_list[o]['nw_fm']=0
		self.building_group.update(self,map,screen)
		self.bio_group.update(self,map,screen)
		if not map.m_planet:
			self.dis=False
			map.display_surface.blit(self.image,self.rect)
		else:
			if map.planet_obj.xy==self.xy:
				self.dis=True