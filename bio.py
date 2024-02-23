import pygame,tile,random,function,setting,text,building,tile
import worker,scientist,gun
pygame.font.init()
font2=pygame.font.Font('NotoSerifCJK-Regular.ttc',18)
class human(pygame.sprite.Sprite):
	def __init__(self,xy,planet,O=None):
		pygame.sprite.Sprite.__init__(self)
		self.surface=pygame.image.load('texture/人类/surface.png')
		self.image=self.surface
		self.head,self.body,self.leg=0,0,0
		self.sex=random.randint(0,1)
		self.type='bio'
		self.choose_time=random.randint(35,45)*30
		if self.sex==0:self.hair=0 
		else: self.hair=1
		self.rect=self.image.get_rect()
		self.rect.topleft=xy
		self.target_x,self.target_y=None,None
		self.e_obj,self.w_obj=None,None
		self.tech_num=0
		self.image,self.outdoor=self.surface,True
		self.image.blit(tile.human_head[0],(0,0))
		self.image.blit(tile.human_hair[self.hair],(0,0))
		self.image.blit(tile.human_body[0],(0,8))
		self.image.blit(tile.human_leg[0],(0,20))
		self.image=pygame.transform.scale(self.image,(20,50))
		self.state,self.action=[],[]
		self.gun_pd=[random.random()+0.1,random.random()+0.05,random.random(),random.random()]#步枪 冲锋枪 狙击枪 轻机枪优先级
		o=0
		for i in self.gun_pd:o+=i
		self.gun_pd=[i/o for i in self.gun_pd]
		self.develop=[random.randint(1,100),random.randint(1,100),random.randint(1,100)]#发展倾向 工科军
		self.follow_obj=None#追随目标
		self.b_obj=None#同意加入目标
		self.O=O#所属组织
		self.fm_obj,self.kill_num=None,0
		self.water_obj=None
		self.water=0
		self.eat_state=None
		self.f_time=random.randint(10,20)#饥饿忍耐上限
		name=''
		for _ in range(random.randint(2,4)):name+=str(random.choice(text.planet_name))
		self.name=name
		self.speech_time,self.speech_maxtime,self.b_speech=0,None,[]
		self.c_obj=None
		self.r_obj=None
		self.army=None
		self.energy_inc=random.uniform(0.7,0.9)
		self.energy=[300,300+random.randint(-100,100)]
		#人类属性
		self.hp,self.hunger,self.cl,self.job,self.age,self.z,self.speed,self.d,self.e,self.g,self.a_z=[100,100],100,random.randint(5,100),[],0,random.randint(0,100),random.uniform(4,5),random.randint(5,100),random.randint(350,450),random.randint(0,100),random.randint(0,100)
		 #生命值 饱食度 智慧 职业 年龄 政治能力 移动速度 胆量 视力 管理能力 指挥能力
	def update(self,planet,map,screen):
		if self.age<=18:self.image=pygame.transform.scale(self.image,(int(20*0.05*self.age),int(50*0.05*self.age)))
		if planet.dis and self.outdoor:self.draw(map,screen,planet)
		if not map.pause:
			#工作精力
			if self.energy[0]<self.energy[1]:self.energy[0]+=self.energy_inc
			#移动
			if 'move' in self.state and (self.target_x or self.target_x==0):self.move(planet)
			elif not self.action and random.random()>0.95:self.random_move(self.rect.x,self.rect.y,-80,80)
			#吃东西优先
			if self.hunger<=self.f_time and not self.eat_state:self.eat_state=True
			if self.eat_state:self.eat(planet,map)
			#游说
			c=0.35-len(planet.O_list)*0.11#加成35% 星球上每有一个组织就-11%
			if not self.O and random.random()*0.3+self.z*0.006+c>0.98 and not 'speech'in self.action and not self.b_obj:self.speech(planet)
			if 'speech'in self.action:self.speech_state(map,planet)
			if 'follow'in self.action:self.follow()
			if 'spread'in self.action:self.spread(map,planet)
			#发展规划
			if 'leader'in self.job and (not planet.O_list[self.O]['develop'] or self.choose_time<=0):
				self.develop_set(planet,map)
				self.choose_time=random.randint(35,45)*20
			if self.O:self.choose_time-=1
			#职业选择
			if self.O and not 'leader'in self.job and not 'soldier'in self.job and (self.choose_time<=0 or not self.job):
				self.job_choose(planet)
				self.choose_time=random.randint(40,45)*20+random.randint(-8,8)
			#职业行为
			if ('water'in self.action or 'water2'in self.action) and not 'move'in self.state:self.water_state(planet)
			elif 'farmer'in self.job and not 'move' in self.state and not 'c_build'in self.action:self.farm(planet,map)
			if 'work'in self.action and self.outdoor:worker.work_check(self)
			if 'work'in self.action and not 'move'in self.state:worker.work(self,planet)
			elif 'worker'in self.job and not 'move'in self.state and not 'c_build'in self.action:worker.build(self,planet,font2)
			
			if 'research'in self.action and self.outdoor:scientist.research_check(self)
			if 'research'in self.action and not 'move'in self.state:scientist.research(self,planet)
			elif 'scientist'in self.job and not 'move'in self.state and not 'c_build'in self.action:scientist.build(self,planet,font2)
			if 'c_build'in self.action and not 'move'in self.state:self.c_build()
			#自然变化
			if self.hunger<=0:self.hp[0]-=0.02+random.random()*0.001
			else:self.hunger-=0.01+random.random()*0.001
			if self.hp[0]<=0:
				planet.bio_group.remove(self)
				if self.O and not 'leader'in self.job:planet.O_list[self.O]['people'].remove(self)
				elif 'leader'in self.job:planet.O_list[self.O]['leader']=random.choice(planet.O_list[self.O]['people'])
				if self.b_obj:self.b_obj.b_speech.remove(self)
				self.job_choose(planet,True)
				if self.army:self.army.soldiers.remove(self)
				del(self)
	def draw(self,map,screen,planet):#渲染
		action=[]
		#调试用
		#pygame.draw.circle(screen, (0, 0, 0), (self.rect.centerx+map.p_vx,self.rect.centery+map.p_vy),self.e,1)#视野范围
		if self.target_x and setting.line:pygame.draw.line(screen,(255,0,0),(self.rect.topleft[0]+map.p_vx,self.rect.topleft[1]+map.p_vy),(self.target_x+map.p_vx,self.target_y+map.p_vy))
		#for i in self.search(planet):pygame.draw.line(screen,(0,60,0),(self.rect.topleft[0]+map.p_vx,self.rect.topleft[1]+map.p_vy),(i.rect.x+map.p_vx,i.rect.y+map.p_vy))#可见人类绘制
		#if self.b_obj:pygame.draw.line(screen,(50,255,40),(self.rect.x+map.p_vx,self.rect.y+map.p_vy),(self.b_obj.rect.x+map.p_vx,self.b_obj.rect.y+map.p_vy))
		#if self.O and planet.O_list[self.O]['leader']!=self:pygame.draw.line(screen,(50,255,40),(self.rect.x+map.p_vx,self.rect.y+map.p_vy),(planet.O_list[self.O]['leader'].rect.x+map.p_vx,planet.O_list[self.O]['leader'].rect.y+map.p_vy))
		if self.O:screen.blit(planet.O_list[self.O]['flag'],(self.rect.centerx+map.p_vx-15,self.rect.centery+map.p_vy-70))
		#-----
		y=-30
		if 'speech' in self.action:action.append('游说')
		if 'follow'in self.action:action.append('追随')
		if 'spread'in self.action:action.append('宣传')
		if 'water'in self.action:action.append('取水')
		if 'water2'in self.action:action.append('灌溉')
		if 'work'in self.action:action.append('工作')
		action.append(str(self.job))
		if action:
			for action_name in action:
				y-=20
				text=font2.render((action_name),False,(250,250,250),(1,100,1))
				screen.blit(text,(self.rect.centerx+map.p_vx-15,self.rect.centery+map.p_vy-50+y))
		text=font2.render((self.name),False,(130,250,250))
		screen.blit(text,(self.rect.centerx+map.p_vx-15,self.rect.centery+map.p_vy-50))
		screen.blit(self.image,(self.rect.topleft[0]+map.p_vx,self.rect.topleft[1]+map.p_vy))
	def search(self,planet):#返回视野内的人类
		result=pygame.sprite.spritecollide(function.Rect((self.e*2,self.e*2),(self.rect.centerx-self.e,self.rect.centery-self.e)),planet.bio_group,False,pygame.sprite.collide_circle)
		return result
	def speech(self,planet):#游说 (开始游说行为 游说范围内的人类被说服则同意加入/跟随/跟随并宣传游说者 游说结束后将被说服者加入组织)
		self.action.append('speech')
	def speech_state(self,map,planet):#游说状态
		if random.random()>0.9 and not('move' in self.state):
			t_obj=random.choice(list(planet.bio_group))
			self.random_move(t_obj.rect.x,t_obj.rect.y,-120,120)#略微增加游走范围与频率 并随机选择游走目标
		if self.speech_time<=0:self.speech_time=int(380*(random.random()*0.8+(1-self.z*0.01)))#发动说服冷却
		if not self.speech_maxtime:self.speech_maxtime=int(600*(1+(random.random()*0.1+self.z*0.01)))#游说的时间
		self.speech_time-=1*setting.civ_debug
		self.speech_maxtime-=1*setting.civ_debug
		if self.speech_maxtime>0:
			if self.speech_time<=0:
				for i in pygame.sprite.spritecollide(function.Rect((self.z*8,self.z*8),(self.rect.centerx-self.z*8,self.rect.centery-self.z*8)),planet.bio_group,False,pygame.sprite.collide_circle):
					if i.b_obj!=self and i!=self:i.if_join(self,self,map,planet)
		else:
			self.stop_speech(planet,map)
	def stop_speech(self,planet,map):#结束游说
		self.speech_maxtime,self.speech_time=None,0
		self.action.remove('speech')
		if self.b_speech:
			if self.b_speech:
				if not self.O:
					O=self.setup_d(self,planet)
					self.O=ascii(O['name'])
					planet.O_list[self.O]=O
					map.info_list[len(map.info_list)+1]=['组织'+O['name']+f'已被{self.name}建立,人数{len(self.b_speech)+1}',setting.time*60,planet.O_list[self.O]['flag']]
				for p in self.b_speech:
					p.O=self.O
					if 'follow'in p.action:p.action.remove('follow')
					if 'spread'in p.action:p.action.remove('spread')
			if self.O:
				planet.O_list[self.O]['people'].extend(self.b_speech)
				self.b_speech=[]
	def setup_d(self,leader,planet):#建立组织
		name=''
		for _ in range(random.randint(2,4)):name+=str(random.choice(text.planet_name))
		O={
		'name':name,
		'leader':leader,
		'people':[],#人员
		'planet':planet,#分布星球
		'fm_group':pygame.sprite.Group(),
		'building_group':pygame.sprite.Group(),
		'fac_group':pygame.sprite.Group(),
		'rs_group':pygame.sprite.Group(),
		'develop':[],#发展优先级(农业,生产(工业),科研,军事)
		'inf':0,#影响力
		'nw_fm':0,#缺水的农田
		'food':0,#食物量
		'army':[],
		'flag':random.choice(tile.flag).convert(),
		'gun_pd':self.gun_pd,#枪械生产优先级
		'gun_list':[],#枪械生产模板
		'iron':0,#铁
		'gun':[],
		'ammo':0,
		'produce':[],#生产资源优先级(从铁开始)
		'tech_num':0,
		'tech':[
		[#农业
		5,#取水速度
		5,#灌溉速度
		8,#食物产量
		5,#食物质量
		1#作物生长速度
		],
		[#工业
		3,#容量
		0.5,#生产速度
		5#产量
		]
		]
		}
		leader.job.append('leader')
		return O
	def if_join(self,s_obj,target,map,planet):#判断是否被说服(说服者 说服者目的)
		B=False
		c=(self.z-s_obj.z)*0.003#政治天赋差距 越大越难被说服
		if c<-0.18:c=0#差距过大 则差距也可以作为增益
		if 'speech'in self.action:c+=0.05#自己也在游说 被说服概率-5%
		if self.O:c+=0.05#已经有组织 说服成功-5%
		if self.O and 'leader'in self.job:c+=100#已经有组织且为领导 则不可能成功
		if random.random()+s_obj.z*0.002-c>0.9:#被说服
			B=True
			if self.b_obj and self in self.b_obj.b_speech:self.b_obj.b_speech.remove(self)
			target.b_speech.append(self)
			self.b_obj=target
			if self.O:#已经有组织,准备脱离
				planet.O_list[self.O]['people'].remove(self)
				self.O=None
				self.action.clear()
				if self.fm_obj and self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
				self.job.clear()
			if 'speech'in self.action:#如果游说途中
				self.action.remove('speech')
				self.speech_maxtime,self.speech_time=None,0
				for p in self.b_speech:
					if not p.if_join(self,s_obj,map,planet):#不同意 都不跟了
						p.b_obj,p.follow_obj=None,None
						if 'follow'in p.action:p.action.remove('follow')
						if 'spread'in p.action:p.action.remove('spread')
				self.b_speech.clear()
			if random.random()+s_obj.z*0.002-c>0.85:#被说服并追随
				if not 'follow'in self.action:self.action.append('follow')
				self.follow_obj=target
				if random.random()+s_obj.z*0.002-c>0.85:#被说服并追随并帮助宣传
					if not 'spread'in self.action:self.action.append('spread')
		return B
	def follow(self):#追随
		if not 'move'in self.state:self.random_move(self.follow_obj.rect.x,self.follow_obj.rect.y,-80,80)
	def spread(self,map,planet):#宣传 效果与游说相同 但是比游说效果差 宣传直至追随目标停止游说
		if self.speech_time<=0:self.speech_time=int(400*(random.random()*0.7+(1-self.z*0.01)))
		self.speech_time-=1
		if self.speech_time<=0:
			for i in pygame.sprite.spritecollide(function.Rect((self.z*7,self.z*7),(self.rect.centerx-self.z*7,self.rect.centery-self.z*7)),planet.bio_group,False,pygame.sprite.collide_circle):
				if i.b_obj!=self.follow_obj and i!=self and i!=self.follow_obj:i.if_join(self,self.b_obj,map,planet)
	def random_move(self,targetx,target_y,min,max):#基于目标点的随机移动(在目标点附近设立随机目标)
		t_x,t_y=int((targetx+random.randint(min,max)*(1+self.d/100))),int((target_y+random.randint(min,max)*(1+self.d/100)))
		self.target_x,self.target_y=t_x,t_y
		if not 'move'in self.state:self.state.append('move')
	def move(self,planet):#移动
		if not(self.target_x<0 or self.target_x>planet.b_map.get_width() or self.target_y<0 or self.target_y>planet.b_map.get_height()):self.rect.topleft=function.move_q(self.rect.topleft[0],self.rect.topleft[1],self.target_x,self.target_y,self.speed)
		elif 'follow'in self.action:self.random_move(self.follow_obj.rect.x,self.follow_obj.rect.y,-80,80)
		else:self.random_move(self.rect.x,self.rect.y,-80,80)
		if self.rect.topleft==(self.target_x,self.target_y):
			self.state.remove('move')
			self.target_x,self.target_y=None,None
	def develop_set(self,planet,map):#优先级规划
		#农业
		food_z=planet.O_list[self.O]['food']+random.randint(-50,50)*(1-self.g/100)
		food_j=100*(len(planet.O_list[self.O]['people'])+1)
		planet.O_list[self.O]['develop'].clear()
		f=int(100-(food_z-food_j)/10)
		if f<0:f=1
		planet.O_list[self.O]['develop'].append(f)
		#生产(工业)与科研与军事
		planet.O_list[self.O]['develop'].extend(self.develop)
		#计算比例
		J,j=0,[]
		if f>90:planet.O_list[self.O]['develop'][0]=10000
		for i in planet.O_list[self.O]['develop']:J+=i
		for i2 in planet.O_list[self.O]['develop']:
			j.append(i2/J)
		planet.O_list[self.O]['develop'].clear()
		planet.O_list[self.O]['develop'].extend(j)
		#工厂生产优先级规划
		J=planet.O_list[self.O]['iron']+len(planet.O_list[self.O]['gun'])+planet.O_list[self.O]['ammo']
		if J==0:J=1
		j.clear()
		j.append(1-(planet.O_list[self.O]['iron'])/J+random.random()*0.01+0.1)
		j.append(1-(len(planet.O_list[self.O]['gun']))/J+random.random()*0.01+0.1)
		j.append(1-(planet.O_list[self.O]['ammo'])/J+random.random()*0.01+0.2)
		planet.O_list[self.O]['produce'].clear()
		planet.O_list[self.O]['produce'].extend(j)
		self.job.clear()
		self.job.append('leader')
		map.info_list[len(map.info_list)+1]=[f'粮食消耗量:{food_j} 粮食产量:'+str(planet.O_list[self.O]['food'])+' 未灌溉农田数:'+str(planet.O_list[self.O]['nw_fm'])+'影响力:'+str(int(planet.O_list[self.O]['inf'])),setting.time*60,planet.O_list[self.O]['flag']]
		map.info_list[len(map.info_list)+1]=[str(planet.O_list[self.O]['name'])+'进行了改革:农工科军'+str([str(int(100*i))+'%' for i in planet.O_list[self.O]['develop']]),setting.time*60,planet.O_list[self.O]['flag']]
		map.info_list[len(map.info_list)+1]=['生产优先级铁枪弹'+str([str(int(100*i))+'%' for i in planet.O_list[self.O]['produce']]),setting.time*60,planet.O_list[self.O]['flag']]
		map.info_list[len(map.info_list)+1]=['铁:'+str(planet.O_list[self.O]['iron'])+'枪:'+str(len(planet.O_list[self.O]['gun']))+'弹药:'+str(planet.O_list[self.O]['ammo']),setting.time*60,planet.O_list[self.O]['flag']]
	def job_choose(self,planet,u=False):#选择职业 (参数2 仅清空职业,不做选择)
		if self.fm_obj and self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
		if 'work'in self.action and not self.outdoor:
			self.w_obj.people[0]-=1
			self.outdoor=True
		if 'research'in self.action and not self.outdoor:
			self.r_obj.people[0]-=1
			self.outdoor=True
		self.job.clear()
		self.action.clear()
		if not u:
			if random.random()<planet.O_list[self.O]['develop'][0]:self.job.append('farmer')
			elif random.random()<planet.O_list[self.O]['develop'][1]:self.job.append('worker')
			elif random.random()<planet.O_list[self.O]['develop'][2]+self.tech_num/100:self.job.append('scientist')
	def c_build(self):#持续建造
		if self.c_obj.jd:self.c_obj.jd[0]+=0.05*setting.build_debug
		else:#建造完成
			self.action.remove('c_build')
	def water_state(self,planet):#取水/灌溉状态
		if 'water'in self.action:
			self.water+=planet.O_list[self.O]['tech'][0][0]
			if not self.fm_obj.water<=random.randint(80,100):self.action.remove('water')
			elif self.water>=200:
				self.action.remove('water')
				self.action.append('water2')
				if not 'move'in self.state:self.state.append('move')
				self.target_x,self.target_y=self.fm_obj.rect.x,self.fm_obj.rect.y
		if 'water2'in self.action:
			self.water-=planet.O_list[self.O]['tech'][0][1]
			self.fm_obj.water+=planet.O_list[self.O]['tech'][0][1]
			if not self.fm_obj.water<=random.randint(80,100) and self.water<=0:
				self.action.remove('water2')
				if self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
			elif self.water<=0:
				if self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
				self.action.remove('water2')
	def farm(self,planet,map):#种田行为
		bd=None
		j=False
		for bd in planet.O_list[self.O]['fm_group']:
			if bd.jd:#耕田
				self.action.append('c_build')
				self.c_obj=bd
				if not 'move'in self.state:self.state.append('move')
				self.target_x,self.target_y=self.c_obj.rect.x,self.c_obj.rect.y
				j=True
				break
			elif bd.water<=150 and random.random()>0.01+len(bd.water_bio)*0.2:#99%灌溉 每已有一个人灌溉概率-20%
				j=True
				if planet.area_group:
					j_dict,j_list={},[]
					for water in planet.area_group:
						j_dict[int(water.rect.x-self.rect.x+water.rect.y-self.rect.y)]=water
						j_list.append(int(water.rect.x-self.rect.x+water.rect.y-self.rect.y))
					water=j_dict[sorted(j_list)[0]]#最近的水域
					self.action.append('water')
					self.fm_obj=bd
					self.fm_obj.water_bio.append(self)
					self.water_obj=water
					if not 'move'in self.state:self.state.append('move')
					self.target_x,self.target_y=self.water_obj.rect.x,self.water_obj.rect.y
				break
		if not j:#没有找到事做 说明没有田或者田的水已经足够
			if random.random()+0.2*planet.O_list[self.O]['nw_fm']<planet.O_list[self.O]['develop'][0] and self.water<=0:#建造新农田
				for bd in planet.O_list[self.O]['fm_group']:
					#四向耕种 上下左右
						xy,j=None,True
						if bd.u and not bd.rect.y-50>setting.map_size[1] and not bd.rect.y-50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x,bd.rect.y-50)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x,bd.rect.y-50)),planet.area_group,False):xy=bd.rect.x,bd.rect.y-50
						elif bd.d and not bd.rect.y+50>setting.map_size[1] and not bd.rect.y+50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x,bd.rect.y+50)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x,bd.rect.y+50)),planet.area_group,False):
							xy=bd.rect.x,bd.rect.y+50
							bd.u=False
						elif bd.l and not bd.rect.x-50>setting.map_size[0] and not bd.rect.x-50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x-50,bd.rect.y)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x-50,bd.rect.y)),planet.area_group,False):
							xy=bd.rect.x-50,bd.rect.y
							bd.d=False
						elif bd.r and not bd.rect.x+50>setting.map_size[0] and not bd.rect.x+50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x+50,bd.rect.y)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(bd.rect.x+50,bd.rect.y)),planet.area_group,False):
							xy=bd.rect.x+50,bd.rect.y
							bd.l=False
						else:
							bd.r=False
						if xy:
							fm=building.fm(xy,self.O)
							function.building_add(self,fm,planet)
							break
				if not j:#没有田可以参考 则随机找个地方建
					xy=None
					if not self.rect.y-50>setting.map_size[1] and not self.rect.y-50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y-50)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y-50)),planet.area_group,False):xy=self.rect.x,self.rect.y-50
					elif not self.rect.y+50>setting.map_size[1] and not self.rect.y+50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y+50)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y+50)),planet.area_group,False):xy=self.rect.x,self.rect.y+50
					elif not self.rect.x-50>setting.map_size[1] and not self.rect.x-50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x-50,self.rect.y)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x-50,self.rect.y)),planet.area_group,False):xy=self.rect.x-50,self.rect.y
					elif not self.rect.x+50>setting.map_size[1] and not self.rect.x+50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x+50,self.rect.y)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x+50,self.rect.y)),planet.area_group,False):xy=self.rect.x+50,self.rect.y
					if xy:
						fm=building.fm(xy,self.O)
						function.building_add(self,fm,planet)
					else:
						self.random_move(self.rect.x,self.rect.y,-90,90)
			elif bd and planet.area_group:#持续灌溉
				bd=random.choice(list(planet.O_list[self.O]['fm_group']))
				j_dict,j_list={},[]
				for water in planet.area_group:
					j_dict[int(water.rect.x-self.rect.x+water.rect.y-self.rect.y)]=water
					j_list.append(int(water.rect.x-self.rect.x+water.rect.y-self.rect.y))
				water=j_dict[sorted(j_list)[0]]#最近的水域
				self.fm_obj=bd
				self.fm_obj.water_bio.append(self)
				if self.water<=0:
					self.action.append('water')
					self.water_obj=water
					if not 'move'in self.state:self.state.append('move')
					self.target_x,self.target_y=self.water_obj.rect.x,self.water_obj.rect.y
				else:
					self.action.append('water2')
					if not 'move'in self.state:self.state.append('move')
					self.target_x,self.target_y=self.fm_obj.rect.x,self.fm_obj.rect.y
		if self.cl*0.01*0.5>random.random()+random.random():
			function.tech_inc(self,planet,0,map)
			self.tech_num+=1
	def eat(self,planet,map):
		F=False
		if self.O and planet.O_list[self.O]['food']>=0:#组织有吃的
			self.hunger+=1
			planet.O_list[self.O]['food']-=1
			planet.O_list[self.O]['inf']+=0.1
			F=True
			if self.hunger>random.randint(60,80) or planet.O_list[self.O]['food']<=0:self.eat_state=False
		elif self.O:#组织没吃的
			for O in planet.O_list:
				if O!=self.O and planet.O_list[O]['food']>=0:
					F=True
					self.hunger+=1
					planet.O_list[O]['food']-=1
					planet.O_list[O]['inf']+=0.1
					if self.hunger>random.randint(60,80):self.eat_state=False
					if planet.O_list[self.O]['inf']<planet.O_list[O]['inf'] and 'leader'not in self.job:#换组织
						planet.O_list[self.O]['people'].remove(self)
						self.O=O
						planet.O_list[self.O]['people'].append(self)
						self.job.clear()
						self.action.clear()
						if self.fm_obj and self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
						map.info_list[len(map.info_list)+1]=[f'{self.name} 退出原组织并加入了组织 '+planet.O_list[self.O]['name'],setting.time*60,planet.O_list[self.O]['flag']]
					elif 'leader'in self.job and planet.O_list[self.O]['inf']+20<planet.O_list[O]['inf'] and len(planet.O_list[self.O]['people'])<13:
#						map.info_list[len(map.info_list)+1]=[planet.O_list[self.O]['name']+' 已被 '+planet.O_list[O]['name']+' 吞并 ',setting.time*60,planet.O_list[self.O]['flag']]
#						#self.O_h(planet,O)
						pass
					break
		else:#没组织
			for O in planet.O_list:
				if planet.O_list[O]['food']>=0:
					F=True
					self.hunger+=1
					planet.O_list[O]['food']-=1
					planet.O_list[O]['inf']+=0.1
					if self.hunger>random.randint(60,80):self.eat_state=False
					self.O=O
					planet.O_list[self.O]['people'].append(self)
					self.job.clear()
					self.action.clear()
					if self.fm_obj and self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
					map.info_list[len(map.info_list)+1]=[f'离居在外的 {self.name} 加入了组织 '+planet.O_list[self.O]['name'],setting.time*60,planet.O_list[self.O]['flag']]
					break
		if not F and self.O:#全图都没有吃的 种田去
			if not 'farmer'in self.job:self.job.append('farmer')
			self.eat_state=False
	def O_h(self,planet,target):#组织吞并 target为吞并者 self为被吞并者领袖
		planet.O_list[target]['people'].extend(planet.O_list[self.O]['people'])
		planet.O_list[target]['people'].append(self)
		self.action.clear()
		if self.fm_obj and self in self.fm_obj.water_bio:self.fm_obj.water_bio.remove(self)
		planet.O_list[target]['food']+=planet.O_list[self.O]['food']
		for bd in planet.O_list[self.O]['building_group']:
			bd.own_O=target
			bd.water_bio.clear()
			print('building',bd.own_O)
		o=list(planet.O_list[target]['building_group'])
		o.extend(list(planet.O_list[self.O]['building_group']))
		planet.O_list[target]['building_group']=pygame.sprite.Group(o)
		for p in planet.O_list[self.O]['people']:
			p.O=target
			p.job_choose(planet)
			print('people',p.O)
		print(self.O,'……',target)
		self.O=target
		self.job_choose(planet)
		del planet.O_list[self.O]