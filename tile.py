import pygame,os
human_head=[]
for i in range(1):human_head.append(pygame.image.load(f'texture/人类/头/{i}.png'))
human_hair=[]
for i in range(2):human_hair.append(pygame.image.load(f'texture/人类/头发/{i}.png'))
human_body=[]
for i in range(1):human_body.append(pygame.image.load(f'texture/人类/躯干/{i}.png'))
human_leg=[]
human_leg_move=[]
for i in range(1):
	human_leg.append(pygame.image.load(f'texture/人类/腿/{i}.png'))
human_hand=[]
for i in range(1):
	for o in range(1):
		human_hand.append(pygame.image.load(f'texture/人类/手/{i}/{o}.png'))
fm=[]
for i in range(5):fm.append(pygame.image.load(f'texture/建筑/耕地/{i}.png'))
info_image=[]
for i in range(1):info_image.append(pygame.image.load(f'texture/图标/{i}.png'))
flag=[]
folders = [f for f in os.listdir('texture/旗帜/flag/') ]
for i in folders:flag.append(pygame.image.load('texture/旗帜/flag/'+i))
fac=[]
for i in range(2):fac.append(pygame.image.load('texture/建筑/工厂/'+str(i)+'.png'))
rs=[]
for i in range(2):rs.append(pygame.image.load('texture/建筑/研究所/'+str(i)+'.png'))
gun=[]
for i in range(4):gun.append(pygame.image.load('texture/枪械/'+str(i)+'.png'))