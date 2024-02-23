import vnoise,pygame,os,random,numpy as np,area
#预设地图生成器
noise=vnoise.Noise(100)
grass=[pygame.image.load('grass1.png')]
water=[pygame.image.load('water1.png')]
def generate(w,h,scale,land,seed,map):#宽 高 平滑值 陆地占比 种子 地图表面
	noise.seed(seed)
	Land,Sea=0,0
	for y in range(h):
		for x in range(w):
			num=noise.noise2(x*scale,y*scale)
			if num<land:
				map.blit(grass[0],(x,y))
				Land+=1
			else:
				map.blit(water[0],(x,y))
				Sea+=1
	return int(round(Land/(w*h),2)*100),int(round(Sea/(w*h),2)*100)#陆海占星球面积
map_size=(50,50)#地图大小
scale=0.00419#平滑值
land=0.2#陆地占比
seed=123#种子
c_num=90#创建地图个数
map=pygame.Surface(map_size)
current_directory = os.getcwd()
folder_path = os.path.join(str(current_directory),'map_list')
os.makedirs(folder_path,exist_ok=True)
num=len([name for name in os.listdir(folder_path)])
for i in range(c_num):
	#最适宜文明发展的噪声值
	seed=random.randint(0,114514)
	scale=random.uniform(0.0251,0.0419)
	land=random.uniform(0.19,0.28)
	num+=1
	map.fill((0,0,0))
	B=generate(map_size[0],map_size[1],scale,land,seed,map)
	new_file_path = os.path.join(folder_path, f"{num} {B[0]}%_{B[1]}%")
	os.makedirs(new_file_path,exist_ok=True)
	pygame.image.save(map,str(new_file_path)+'/map.png')
	map_array = np.array([[map.get_at((x, y))[:3] for x in range(50)] for y in range(50)])
	closed_water_areas = area.find_closed_water_areas(map_array,50,50)
	area.save_areas_as_images(closed_water_areas,new_file_path)
	open(str(new_file_path+'/info.txt'), 'w').write(f'平滑值:{scale}\n陆地占比:{land}\n随机种子:{seed}')