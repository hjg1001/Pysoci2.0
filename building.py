import pygame,tile,random,function,setting,gun,text,copy
class fm(pygame.sprite.Sprite):
	def __init__(self,xy,O):
		self.own_O=O
		self.type='fm'
		self.u,self.d,self.l,self.r=True,True,True,True#上下左右是否可建造田
		self.jd=[0,100]#建造进度
		self.water_bio=[]#正在准备灌溉这个田的人(避免灌溉冗余) 迷之属性 有时候有用有时候没用
		pygame.sprite.Sprite.__init__(self)
		self.image=tile.fm[0]
		self.rect=self.image.get_rect()
		self.rect.topleft=xy
		self.c_food,self.q_food,self.t_food,self.water=5,20,[0,600],50#一次产食物量 食物质量(加饱食度) 产食物目前时间/所需时间(帧) 灌溉水量
	def update(self,planet,map,screen):
		if self.jd and self.jd[0]>=self.jd[1]:self.jd=None
		if not self.jd and not map.pause:
			#消耗self.water增长 self.t_food[0] self.t_food[0]到达self.t_food[1]时 时间清零,self.food增加self.c_food
			if self.water>0:
				self.water-=planet.O_list[self.own_O]['tech'][0][4]
				self.t_food[0]+=planet.O_list[self.own_O]['tech'][0][4]
			if self.water<100:planet.O_list[self.own_O]['nw_fm']+=1
			if self.t_food[0]>=self.t_food[1]:
				self.t_food[0]=0
				planet.O_list[self.own_O]['food']+=planet.O_list[self.own_O]['tech'][0][2]*planet.O_list[self.own_O]['tech'][0][3]
		self.draw(planet,map,screen)
	def draw(self,planet,map,screen):
		if planet.dis:
			if self.t_food[0]/self.t_food[1]<=0.25:self.image=tile.fm[0].convert()
			if self.t_food[0]/self.t_food[1]>=0.25 and self.t_food[0]/self.t_food[1]<=0.5:self.image=tile.fm[1].convert()
			if self.t_food[0]/self.t_food[1]>=0.5 and self.t_food[0]/self.t_food[1]<=0.75:self.image=tile.fm[2].convert()
			if self.t_food[0]/self.t_food[1]>=0.75:self.image=tile.fm[3].convert()
			if self.jd:self.image=tile.fm[4].convert()
			screen.blit(self.image,(self.rect.topleft[0]+map.p_vx,self.rect.topleft[1]+map.p_vy))
class fac(pygame.sprite.Sprite):
	def __init__(self,xy,O,c_type,font):
		self.type='fac'
		self.own_O=O
		self.c_type=c_type#生产的资源
		pygame.sprite.Sprite.__init__(self)
		self.image=tile.fac[0].convert()
		self.rect=self.image.get_rect()
		self.jd=[0,100]
		self.u,self.d,self.l,self.r=True,True,True,True
		self.c_jd=[0,300]#生产进度
		self.people=[0,3]#容量
		self.rect.topleft=xy
		self.font2=font
		self.g_time=[0,random.randint(10,20)*60]
	def update(self,planet,map,screen):
		if not map.pause:
			if self.g_time[0]>=self.g_time[1]:
				if random.random()<planet.O_list[self.own_O]['produce'][0] or planet.O_list[self.own_O]['produce'][0]>1:
					self.c_type='iron'
				if (random.random()<planet.O_list[self.own_O]['produce'][1] or planet.O_list[self.own_O]['produce'][1]>1 )and planet.O_list[self.own_O]['gun_list']:
					self.c_type='gun'
				if random.random()<planet.O_list[self.own_O]['produce'][2]or planet.O_list[self.own_O]['produce'][2]>1:
					self.c_type='ammo'
			if not self.jd:
				if self.g_time[0]>=self.g_time[1]:self.g_time[0]=0
				self.g_time[0]+=1
			if self.jd and self.jd[0]>=self.jd[1]:self.jd=None
			if self.c_jd[0]>=self.c_jd[1]:
				if self.c_type!='gun':
					self.c_jd[0]=0
					if self.c_type=='ammo':planet.O_list[self.own_O][self.c_type]+=planet.O_list[self.own_O]['tech'][1][2]*3
					else:planet.O_list[self.own_O][self.c_type]+=planet.O_list[self.own_O]['tech'][1][2]
				else:
					if random.random()<planet.O_list[self.own_O]['gun_pd'][0]and self.c_jd[0]>=planet.O_list[self.own_O]['gun_list'][0].cost:
						self.c_jd[0]-=planet.O_list[self.own_O]['gun_list'][0].cost
						planet.O_list[self.own_O]['gun'].append(copy.copy(planet.O_list[self.own_O]['gun_list'][0]))
					if random.random()<planet.O_list[self.own_O]['gun_pd'][1]and self.c_jd[0]>=planet.O_list[self.own_O]['gun_list'][1].cost:
						self.c_jd[0]-=planet.O_list[self.own_O]['gun_list'][1].cost
						planet.O_list[self.own_O]['gun'].append(copy.copy(planet.O_list[self.own_O]['gun_list'][1]))
					if random.random()<planet.O_list[self.own_O]['gun_pd'][2]and self.c_jd[0]>=planet.O_list[self.own_O]['gun_list'][2].cost:
						self.c_jd[0]-=planet.O_list[self.own_O]['gun_list'][2].cost
						planet.O_list[self.own_O]['gun'].append(copy.copy(planet.O_list[self.own_O]['gun_list'][2]))
					if random.random()<planet.O_list[self.own_O]['gun_pd'][3]and self.c_jd[0]>=planet.O_list[self.own_O]['gun_list'][3].cost:
						self.c_jd[0]-=planet.O_list[self.own_O]['gun_list'][3].cost
						planet.O_list[self.own_O]['gun'].append(copy.copy(planet.O_list[self.own_O]['gun_list'][3]))
		if planet.dis:
			if not self.jd:self.image=tile.fac[1].convert()
			screen.blit(self.image,(self.rect.x+map.p_vx,self.rect.y+map.p_vy))
			screen.blit(self.font2.render(str(self.people[0])+'/'+str(self.people[1])+str(self.c_type)+str(int(self.c_jd[0])),False,(250,250,250)),(self.rect.x+map.p_vx,self.rect.y+map.p_vy))

class rs(pygame.sprite.Sprite):
	def __init__(self,xy,O,font):
		self.type='rs'
		self.own_O=O
		pygame.sprite.Sprite.__init__(self)
		self.image=tile.rs[0].convert()
		self.rect=self.image.get_rect()
		self.jd=[0,100]
		self.u,self.d,self.l,self.r=True,True,True,True
		self.s_jd=[0,100]#武器设计进度
		self.c_jd=[0,100]#科研进度
		self.people=[0,5]#容量
		self.produce=[]
		self.rect.topleft=xy
		self.font2=font
	def update(self,planet,map,screen):
		if not map.pause:
			if self.people[0]<0:self.people[0]=0
			if self.jd and self.jd[0]>=self.jd[1]:self.jd=None
			if self.c_jd[0]>=self.c_jd[1]:
				self.c_jd[0]=0
				c_num=random.randint(1,5)
				tech,tech_name=random.randint(0,1),['农业','工业']
				for _ in range(c_num):function.tech_inc(self,planet,tech,map)
				map.info_list[len(map.info_list)+1]=[str(c_num)+'项%s研究已经完成'%tech_name[tech],setting.time*60,planet.O_list[self.own_O]['flag']]
				planet.O_list[self.own_O]['tech_num']+=c_num
				self.c_jd[1]+=7*c_num#每突破一次阈值就提高一次阈值 避免科技爆炸
			elif self.s_jd[0]>=self.s_jd[1]:
				self.s_jd[0]=0
				if not planet.O_list[self.own_O]['gun_list']:
					planet.O_list[self.own_O]['gun_list'].append(gun.Gun(random.choice(text.Gun)+'步枪',planet.O_list[self.own_O]['flag'],180,1,10,20,0,60,5,100))
					planet.O_list[self.own_O]['gun_list'].append(gun.Gun(random.choice(text.Gun)+'冲锋枪',planet.O_list[self.own_O]['flag'],200,10,5,20,1,10,50,210))
					planet.O_list[self.own_O]['gun_list'].append(gun.Gun(random.choice(text.Gun)+'狙击步枪',planet.O_list[self.own_O]['flag'],180,1,60,25,2,180,50,200))
					planet.O_list[self.own_O]['gun_list'].append(gun.Gun(random.choice(text.Gun)+'轻机枪',planet.O_list[self.own_O]['flag'],250,30,8,3,3,8,50,300))
				else:
					num=random.randint(1,5)
					for _ in range(num):
						tech=random.randint(0,5)
						gun_id=random.randint(0,3)
						if tech==0:
							planet.O_list[self.own_O]['gun_list'][gun_id].damage+=random.random()
						elif tech==1:
							planet.O_list[self.own_O]['gun_list'][gun_id].ammo[1]+=random.randint(0,1)
						elif tech==2:
							planet.O_list[self.own_O]['gun_list'][gun_id].z+=random.randint(0,1)
						elif tech==3 and planet.O_list[self.own_O]['gun_list'][gun_id].s_time[1]>0.1:
							planet.O_list[self.own_O]['gun_list'][gun_id].s_time[1]-=random.random()*0.1
						elif tech==4:
							planet.O_list[self.own_O]['gun_list'][gun_id].n+=random.random()*0.5
						elif planet.O_list[self.own_O]['gun_list'][gun_id].reload[1]>0.01:
							planet.O_list[self.own_O]['gun_list'][gun_id].reload[1]-=random.random()*0.1
					map.info_list[len(map.info_list)+1]=[str(num)+'项枪械研究已经完成',setting.time*60,planet.O_list[self.own_O]['flag']]
					planet.O_list[self.own_O]['tech_num']+=num
					self.s_jd[1]+=num*5
		if planet.dis:
			if not self.jd:self.image=tile.rs[1].convert()
			screen.blit(self.image,(self.rect.x+map.p_vx,self.rect.y+map.p_vy))
			screen.blit(self.font2.render(str(self.people[0])+'/'+str(self.people[1])+' '+str(int(self.c_jd[0])),False,(250,250,250)),(self.rect.x+map.p_vx,self.rect.y+map.p_vy))