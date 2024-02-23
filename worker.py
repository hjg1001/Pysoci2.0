#写农民行为逻辑写了几百行 频繁使用搜索和跳转 才意识到没分文件的严重性
import function,setting,pygame,building
#工人-建造工厂或进入工厂工作
def build(self,planet,font):#建造 可以照搬农民耕田行为
	j=False
	for bd in planet.O_list[self.O]['fac_group']:
		if bd.jd:#继续建造
			self.action.append('c_build')
			self.c_obj=bd
			if not 'move'in self.state:self.state.append('move')
			self.target_x,self.target_y=self.c_obj.rect.centerx,self.c_obj.rect.centery
			j=True
			break
		elif bd.people[0]<bd.people[1] and self.energy[0]>=self.energy[1]:#有空间和精力 去工作
			j=True
			if not 'work'in self.action:self.action.append('work')
			if not 'move'in self.state:self.state.append('move')
			self.w_obj=bd
			self.target_x,self.target_y=bd.rect.centerx,bd.rect.centery
	if not j and self.energy[0]>=self.energy[1]:#没有工厂 或者 没有空闲工厂 则建造新的
		for bd in planet.O_list[self.O]['fac_group']:
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
					fm=building.fac(xy,self.O,'iron',font)
					function.building_add(self,fm,planet)
					break
		if not j:
			xy=None
			if not self.rect.y-50>setting.map_size[1] and not self.rect.y-50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y-50)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y-50)),planet.area_group,False):xy=self.rect.x,self.rect.y-50
			elif not self.rect.y+50>setting.map_size[1] and not self.rect.y+50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y+50)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x,self.rect.y+50)),planet.area_group,False):xy=self.rect.x,self.rect.y+50
			elif not self.rect.x-50>setting.map_size[1] and not self.rect.x-50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x-50,self.rect.y)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x-50,self.rect.y)),planet.area_group,False):xy=self.rect.x-50,self.rect.y
			elif not self.rect.x+50>setting.map_size[1] and not self.rect.x+50<0 and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x+50,self.rect.y)),planet.building_group,False)and not pygame.sprite.spritecollide(function.Rect((50,50),(self.rect.x+50,self.rect.y)),planet.area_group,False):xy=self.rect.x+50,self.rect.y
			if xy:
				j=True
				fm=building.fac(xy,self.O,'iron',font)
				function.building_add(self,fm,planet)
def work(self,planet):#工作
	if self.outdoor:self.w_obj.people[0]+=1
	self.outdoor=False
	if self.w_obj.c_type!='gun':self.w_obj.c_jd[0]+=planet.O_list[self.O]['tech'][1][1]
	else:self.w_obj.c_jd[0]+=planet.O_list[self.O]['tech'][1][1]*0.8
	self.energy[0]-=1
	if self.energy[0]<=0:
		self.action.remove('work')
		self.outdoor=True
		self.w_obj.people[0]-=1
def work_check(self):#检查工厂是否已满
	if self.w_obj.people[0]==self.w_obj.people[1]:
		self.action.remove('work')
		if 'move' in self.state:self.state.remove('move')
		self.target_x,self.target_y=None,None