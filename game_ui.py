import pygame,UI,setting
pygame.init()
font=pygame.font.Font('NotoSerifCJK-Regular.ttc',15)
font2=pygame.font.Font('NotoSerifCJK-Regular.ttc',20)
font3=pygame.font.Font('NotoSerifCJK-Regular.ttc',30)
j_x,j_y=setting.screen_size[0]//2,setting.screen_size[1]//2#屏幕中央
#主UI(最顶上的)
def off_s_map():
	setting.s_map=not setting.s_map
def off_planet_map(map):
	map.m_planet=False
	map.planet_obj=False
def b0(map):
	map.ui3_state=True
	if map.ui2_state:
		map.ui2_state=False
		map.planet_obj=False
text1=UI.Text(0,font,0,0,color=(255,255,255))
text2=UI.Text(0,font,0,15,color=(255,255,255))
button1=UI.Button(60,0,60,45,'小地图',font2,(255,255,255),(0,0,0),off_s_map)
button2=UI.Button(125,0,60,45,'宇宙视图',font2,(255,255,255),(0,0,0))
button3=UI.Button(190,0,60,45,'文明',font2,(255,255,255),(0,0,0),b0)
def ui1(fps,map):
	u_list=[]
	text1.text=f'fps{int(fps)}'
	u_list.append(text1)
	text2.text=''
	if map.pause:text2.text='暂停'
	u_list.append(text2)
	if setting.s_map:button1.text_color=(0,180,0)
	else:button1.text_color=(0,0,0)
	u_list.append(button1)
	if map.m_planet:
		button2.text='退出'
		button2.text_color=(210,8,6)
		button2.action=off_planet_map
		button2.action_r=map
	else:
		button2.action=None
		button2.text='宇宙'
		button2.text_color=(0,0,0)
	u_list.append(button2)
	button3.action_r=map
	u_list.append(button3)
	ui_1=UI.ui(u_list,0,0,setting.screen_size[0],45,color=(0,0,255))
	return ui_1
#UI2-星球简介
ui2_u_list=[]
ui2_img1=UI.Image(None,j_x-250,j_y-250)
ui2_img2=UI.Image(None,j_x-250,j_y-50)
ui2_text1=UI.Text(0,font,j_x-170,j_y-245,color=(255,255,255))
ui2_text2=UI.Text(0,font,j_x-170,j_y-230,color=(255,255,255))
def b1(map):
	map.ui2_state=False
	map.planet_obj=None
def b2(map):
	map.ui2_state=False
	map.m_planet=True
ui2_button1=UI.Button(j_x+200,j_y-250,50,45,'关闭',font2,(0,0,0),(255,0,0),b1)
ui2_button2=UI.Button(j_x-250,j_y-165,50,45,'视图',font2,(255,255,255),(0,0,0),b2)
def ui2(map):
	ui2_u_list.clear()
	ui2_img1.img=pygame.transform.scale(map.planet_obj.image,(80,80))
	ui2_u_list.append(ui2_img1)
	ui2_img2.img=pygame.transform.scale(map.planet_obj.map,(500,300))
	ui2_u_list.append(ui2_img2)
	ui2_text1.text=f'名称:{map.planet_obj.name}'
	ui2_u_list.append(ui2_text1)
	ui2_text2.text=f'大小:{map.planet_obj.map_size[0]}*{map.planet_obj.map_size[1]}'
	ui2_u_list.append(ui2_text2)
	ui2_button1.action_r=map
	ui2_u_list.append(ui2_button2)
	ui2_button2.action_r=map
	ui2_u_list.append(ui2_button1)
	ui_2=UI.ui(ui2_u_list,j_x-250,j_y-250,500,500,color=(64,63,65))
	return ui_2
#UI3-组织界面
def b3(map):
	map.ui3_state=False
def b5(map,g_list):
	if map.ui3_state:map.ui3_state=False
	map.ui4_state=True
	map.ui4_list=g_list
button4=UI.Button(j_x+235,j_y-295,50,45,'关闭',font2,(0,0,0),(255,0,0),b3)
text3=UI.Text('暂无文明',font2,j_x-25,j_y-25,color=(255,255,255))
def ui3(map):
	ui3_u_list=[]
	button4.action_r=map
	ui3_u_list.append(button4)
	y=0
	for pl in map.planet_sprite:
		for o in pl.O_list:
			if o:
				o_list=[]
				o_img=UI.Image(pl.O_list[o]['flag'],j_x-248,j_y-245+y)
				o_list.append(o_img)
				text4=UI.Text(pl.O_list[o]['name'],font,j_x-196,j_y-245+y,color=(5,255,140))
				o_list.append(text4)
				text5=UI.Text('领袖:'+pl.O_list[o]['leader'].name,font,j_x-196,j_y-230+y,color=(5,255,140))
				o_list.append(text5)
				text6=UI.Text('('+str(len(pl.O_list[o]['people'])+1)+')',font,j_x-196+len(text4.text)*15,j_y-245+y,color=(0,255,0))
				o_list.append(text6)
				text5=UI.Text('食物:'+str(int(pl.O_list[o]['food'])),font,text6.rect.topright[0]+15,j_y-245+y,color=(255,189,98))
				o_list.append(text5)
				text4=UI.Text('产能:'+str(int(len(pl.O_list[o]['fac_group'])*pl.O_list[o]['tech'][1][1]*pl.O_list[o]['tech'][1][2])),font,text5.rect.topright[0],text5.rect.topright[1],color=(255,250,255))
				o_list.append(text4)
				text6=UI.Text('科研:'+str(pl.O_list[o]['tech_num']),font,text5.rect.bottomleft[0],text5.rect.bottomleft[1],color=(186,204,255))
				o_list.append(text6)
				button6=UI.Button(text4.rect.topright[0]+10,text4.rect.topright[1],50,40,'枪械',font2,(255,255,255),(0,0,0),b5)
				button6.action_r=map
				button6.action_r2=pl.O_list[o]
				o_list.append(button6)
				o_ui=UI.ui(o_list,j_x-250,j_y-250+y,500,50,(255,255,255),2)
				o_ui.action=True
				ui3_u_list.append(o_ui)
				y+=50
				if y>500:break
	if y==0:
		ui3_u_list.append(text3)
	ui_3=UI.ui(ui3_u_list,j_x-250,j_y-250,500,500,color=(64,63,65))
	return ui_3
#ui4-枪支页面
def b4(map):
	map.ui4_state=False
button5=UI.Button(j_x+235,j_y-295,50,45,'关闭',font2,(0,0,0),(255,0,0),b4)
text7=UI.Text('暂无枪械',font2,j_x-25,j_y-25,color=(255,255,255))
def ui4(map):
	ui4_u_list=[]
	button5.action_r=map
	ui4_u_list.append(button5)
	y=0
	for g in map.ui4_list['gun_list']:
		o_list=[]
		img1=img1=UI.Image(0,j_x-248,j_y-248+y)
		img1.img=pygame.transform.scale(g.image,(160,60))
		o_list.append(img1)
		img_rect=img1.img.get_rect()
		img_rect.topleft=j_x-248,j_y-248+y
		text8=UI.Text('名称:'+g.name,font,img_rect.topright[0],img_rect.topright[1],color=(5,255,5))
		o_list.append(text8)
		text9=UI.Text('威力:'+str(int(g.damage)),font,img_rect.topright[0],img_rect.topright[1]+15,color=(5,255,140))
		o_list.append(text9)
		text10=UI.Text('命中率:'+str(int(g.z))+'%',font,img_rect.topright[0],img_rect.topright[1]+30,color=(5,255,140))
		o_list.append(text10)
		text11=UI.Text('装弹量:'+str(g.ammo[1]),font,img_rect.topright[0],img_rect.topright[1]+45,color=(5,255,140))
		o_list.append(text11)
		text9=UI.Text('射速:'+str(round(g.s_time[1]/60,1))+'秒/发',font,img_rect.topright[0],img_rect.topright[1]+60,color=(5,255,140))
		o_list.append(text9)
		text9=UI.Text('换弹时间:'+str(round(g.reload[1]/60,1))+'秒',font,img_rect.topright[0],img_rect.topright[1]+75,color=(5,255,140))
		o_list.append(text9)
		text9=UI.Text('耐久:'+str(int(g.n)),font,img_rect.topright[0],img_rect.topright[1]+90,color=(5,255,140))
		o_list.append(text9)
		text9=UI.Text('造价:'+str(int(g.cost)),font,img_rect.topright[0],img_rect.topright[1]+105,color=(5,255,140))
		o_list.append(text9)
		text11=UI.Text('库存:'+str([i.name for i in map.ui4_list['gun']].count(g.name)),font3,img_rect.centerx+300,img_rect.centery,color=(5,255,140))
		o_list.append(text11)
		o_ui=UI.ui(o_list,j_x-250,j_y-250+y,500,125,(255,255,255),2)
		o_ui.action=True
		ui4_u_list.append(o_ui)
		y+=125
	if y==0:
		ui4_u_list.append(text7)
	ui_4=UI.ui(ui4_u_list,j_x-250,j_y-250,500,500,color=(64,63,65))
	return ui_4