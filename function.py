import pygame,math,random,setting
def move_q(x, y, target_x, target_y, speed):
    dx = target_x - x
    dy = target_y - y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance <= speed:
        new_x = target_x
        new_y = target_y
    else:
        ratio = speed / distance
        new_x = x + dx * ratio
        new_y = y + dy * ratio
    return new_x,new_y
class Rect(pygame.sprite.Sprite):
	def __init__(self,size,xy):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface(size)
		self.rect=self.image.get_rect()
		self.rect.topleft=xy
def building_add(self,building,planet):
		if building.type=='fm':
			planet.O_list[self.O]['fm_group'].add(building)
			planet.fm_group.add(building)
		elif building.type=='fac':
			planet.O_list[self.O]['fac_group'].add(building)
		elif building.type=='rs':
			planet.O_list[self.O]['rs_group'].add(building)
		planet.O_list[self.O]['building_group'].add(building)
		planet.building_group.add(building)
def tech_inc(self,planet,tech_id,map):#科技增长(随机)
		#农业科技可不靠研究所增长 防止停滞在低级阶段
		if self.type=='bio':tech=random.randint(0,len(planet.O_list[self.O]['tech'][tech_id])-1)
		else:tech=random.randint(0,len(planet.O_list[self.own_O]['tech'][tech_id])-1)
		if tech_id==0:
			if tech==0:
				if self.type=='bio':
					planet.O_list[self.O]['tech'][0][0]+=random.random()*0.15
					map.info_list[len(map.info_list)+1]=[self.name+random.choice(['发现了更好的取水方法','发明了新的取水工具']),setting.time*60,planet.O_list[self.O]['flag']]
				else:
					planet.O_list[self.own_O]['tech'][0][tech]+=random.random()*0.3
			if tech==1:
				if self.type=='bio':
					planet.O_list[self.O]['tech'][0][0]+=random.random()*0.15
					map.info_list[len(map.info_list)+1]=[self.name+random.choice(['发现了更好的灌溉方法','发明了新的灌溉工具']),setting.time*60,planet.O_list[self.O]['flag']]
				else:
					planet.O_list[self.own_O]['tech'][0][tech]+=random.random()*0.3
			if tech==2:
				if self.type=='bio':
					planet.O_list[self.O]['tech'][0][0]+=random.random()*0.15
					map.info_list[len(map.info_list)+1]=[self.name+random.choice(['发现了更高产的作物','发明了更高产的种植方法']),setting.time*60,planet.O_list[self.O]['flag']]
				else:
					planet.O_list[self.own_O]['tech'][0][tech]+=random.random()*0.3
			if tech==3:
				if tech==0:
					if self.type=='bio':
						planet.O_list[self.O]['tech'][0][0]+=random.random()*0.15
						map.info_list[len(map.info_list)+1]=[self.name+random.choice(['发现了更有营养的作物','发明了培育高质量作物的新方法']),setting.time*60,planet.O_list[self.O]['flag']]
					else:
						planet.O_list[self.own_O]['tech'][0][tech]+=random.random()*0.3
			if tech==4:
				if self.type=='bio':
					planet.O_list[self.O]['tech'][0][0]+=random.random()*0.15
					map.info_list[len(map.info_list)+1]=[self.name+random.choice(['发现了生长更快的作物','发明了作物催熟新方法']),setting.time*60,planet.O_list[self.O]['flag']]
				else:
					planet.O_list[self.own_O]['tech'][0][tech]+=random.random()*0.3
		elif tech_id==1:
			if tech==0:
				planet.O_list[self.own_O]['tech'][1][0]+=0.5
				if int(planet.O_list[self.own_O]['tech'][1][0])%planet.O_list[self.own_O]['tech'][1][0]==0:
					#进行建筑全面升级
					for bd in planet.O_list[self.own_O]['building_group']:
						if bd.type!='fm':bd.people[1]+=1
			elif tech==1:
				planet.O_list[self.own_O]['tech'][1][1]+=random.random()*0.3
			elif tech==2:
				planet.O_list[self.own_O]['tech'][1][2]+=random.random()*0.3