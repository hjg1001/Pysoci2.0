import function,setting,pygame,building,random
#科学家-开设研究所或进入研究所工作
#可以照搬工人
def build(self,planet,font):
	j=False
	for bd in planet.O_list[self.O]['rs_group']:
		if bd.jd:
			self.action.append('c_build')
			self.c_obj=bd
			if not 'move'in self.state:self.state.append('move')
			self.target_x,self.target_y=self.c_obj.rect.centerx,self.c_obj.rect.centery
			j=True
			break
		elif bd.people[0]<bd.people[1] and self.energy[0]>=self.energy[1]:#有空间和精力 去工作
			j=True
			if not 'research'in self.action:self.action.append('research')
			if not 'move'in self.state:self.state.append('move')
			self.r_obj=bd
			self.target_x,self.target_y=bd.rect.centerx,bd.rect.centery
	if not j and self.energy[0]>=self.energy[1]:
		for bd in planet.O_list[self.O]['rs_group']:
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
					fm=building.rs(xy,self.O,font)
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
				fm=building.rs(xy,self.O,font)
				function.building_add(self,fm,planet)
def research(self,planet):#工作
	if self.outdoor:self.r_obj.people[0]+=1
	self.outdoor=False
	if planet.O_list[self.O]['develop'][3]>random.random() or not planet.O_list[self.O]['gun_list']:#武器设计
		self.r_obj.s_jd[0]+=0.1+self.cl*0.001
		self.energy[0]-=1
	else:
		self.r_obj.c_jd[0]+=0.1+self.cl*0.001
		self.energy[0]-=1
	if self.energy[0]<=0:
		self.action.remove('research')
		self.outdoor=True
		self.r_obj.people[0]-=1
def research_check(self):#检查是否已满
	if self.r_obj.people[0]==self.r_obj.people[1]:
		self.action.remove('research')
		if 'move' in self.state:self.state.remove('move')
		self.target_x,self.target_y=None,None