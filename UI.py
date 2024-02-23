import pygame
class Button:
    def __init__(self,x,y,width,height,text,font,button_color=(255,255,255),text_color=(0,0,0),action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.button_color = button_color
        self.text_color = text_color
        self.font = font
        self.text = text
        self.action = action
        self.action_r=None
        self.action_r2=None
    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    if self.action_r and( self.action_r2 or self.action_r2==[]):self.action(self.action_r,self.action_r2)
                    elif self.action_r:self.action(self.action_r)
                    else:self.action()
class Image:
	def __init__(self,image,x,y):
		self.img=image
		self.x,self.y=x,y
		self.action=None
	def draw(self,screen):
		screen.blit(self.img,(self.x,self.y))
class Text:
	def __init__(self,text,font,x,y,color=(0,0,0)):
		self.x,self.y=x,y
		self.action=None
		self.font=font
		self.text=text
		self.color=color
		text_surface=self.font.render(str(self.text),True,self.color)
		self.rect=text_surface.get_rect()
		self.rect.topleft=self.x,self.y
	def draw(self,screen):
		text_surface=self.font.render(self.text,True,self.color)
		screen.blit(text_surface,(self.x,self.y))
class ui:
	def __init__(self,u_list,x,y,width,height,color=(66,65,64),w=0):
		self.u_list=u_list
		self.color=color
		self.action=None
		self.rect=pygame.Rect(x,y,width,height)
		self.w=w
	def draw(self,screen):
		pygame.draw.rect(screen,self.color,self.rect,self.w)
		for u in self.u_list:u.draw(screen)
	def event(self,ev):
		for u in self.u_list:
			if u.action:u.event(ev)