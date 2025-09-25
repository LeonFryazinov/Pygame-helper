import pygame
from enum import Enum
import random

class OBJECTS(Enum): #enum
    BASE = 0
    BASE_RECT = 1
    BASE_CIRCLE = 2

#Remember that calling to screen will not allow autocomplete

class Object:  #base object class, used only for inheritance.
    def __init__(self,window,pos,col=pygame.Color(22,252,187,255),rendered = True,render_priority = 100,group=[]):
        self.pos = pos
        self.col = col
        self.rendered = rendered
        self.window = window
        self.UID = window.get_id()
        self.render_priority = render_priority
        self.group = []
    def render_prep(self): # a function that allows for more complex objects to render multiple simpler objects instead of one complex
        pass
    def render(self): # does the "draw" function dependent on object type, overwritten in inherited classes
        pass





class Base_rectangle(Object):  # a simple rectangle
    def __init__(self, window, pos,size,col=pygame.Color(22, 252, 187, 255), rendered=True, render_priority=100,group=[]):
        super().__init__(window, pos, col, rendered, render_priority,group)
        self.size = size
    def render_prep(self):
        return None
    def render(self):
        self.window.draw_rectangle()





class Base_circle(Object): # a simple circle
    def __init__(self, window, pos,rad, col=pygame.Color(22, 252, 187, 255), rendered=True, render_priority=100,group=[]):
        super().__init__(window, pos, col, rendered, render_priority,group)
        self.radius = rad
    def render_prep(self):
        return None
    def render(self):
        self.window.draw_circle(self.pos,self.radius,self.col)


class Image(Object):
    def __init__(self,window,pos,image_path,scale,rendered = True,render_priority = 100,group=[]):
        super().__init__(window,pos,pygame.Color(255,255,255,255),rendered,render_priority,group)
        self.image_surf = pygame.image.load(image_path).convert()
        image_size = (self.image_surf.get_width(),self.image_surf.get_height())
        self.image_surf = pygame.transform.scale(self.image_surf,(image_size[0]*scale[0],image_size[1]*scale[1]))

    def render_prep(self):
        return None
    
    def render(self):
        self.window.draw_image(self.pos,self.image_surf)










class GameWindow: #main window class
    def __init__(self,screen_size=(500,500),caption= "window"):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True
        pygame.display.set_caption(caption)
        self.render_queue = []
        self.object_list = []
        self.current_id = 1000
    def process(self): # to be run every frame
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def add_object(self,obj:Object): # add object to the object list, in the order at which each object will be rendered.
        if len(self.object_list) == 0:
            self.object_list.append(obj)
            return
        for i, OBJ in enumerate(self.object_list):
            if obj.render_priority < OBJ.render_priority:
                self.object_list.insert(i,obj)
                return
            elif i == len(self.object_list)-1:
                self.object_list.append(obj)
                print("added at end")
                return


    def get_id(self): #generates a unique id for every object being created
        self.current_id += 1
        return self.current_id-1
    def prep_render(self): # prepares each object for rendering 
        for obj in self.object_list:
            if obj.rendered:
                obj.render_prep(self)


    def render(self): # draws each object in queue
        for obj in self.render_queue:
            obj.render(self)

    def quit(self): # quit
        self.running = False
        pygame.quit()

    def draw_rect(self,pos:tuple,size:tuple,col = pygame.Color(255,255,255,255)): # draws simple rectange that frame
        pygame.draw.rect(self.screen,col,pygame.Rect((pos[0]-(size[0]/2),pos[1]-(size[1]/2)),size))

    def draw_circle(self,pos:tuple,rad:int,col=pygame.Color(255,255,255,255)): # draws simple circle that frame
        pygame.draw.circle(self.screen,col,pos,rad)

    def draw_image(self,pos:tuple,image_surf):
        self.screen.blit(image_surf,pos)
        









window = GameWindow((600,600),"hello")

while window.running:
    window.process()

