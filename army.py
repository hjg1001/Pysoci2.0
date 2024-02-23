import random
class army:
	def __init__(self,leader,O):
		self.leader=leader
		self.soldiers=[]
		self.O=O#上级
		self.state=None
	def Z(self,planet,num):#招募 数量
		c_num=0
		for p in planet.O_list[self.O]['people']:
			if 'soldier' not in p.job:
				c_num+=1
				self.soldiers.append(p)
				p.job_choose(planet,True)
				p.job.append('soldier')
				p.army=self
			if c_num==num:
				break