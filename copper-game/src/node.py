import pygame
import game

class Node(object):
    def __init__(self):
        self.children = []
        self.parent = None
        self.rect = None
        self.plasma = False
        self.scaling = False
        self.scene_viewed = False
        self.depth = 0
    
    def add(self, n):
        n.parent = self
        self.children.append(n)
    
    def draw_all(self):
        self.draw()
        for child in self.children:
            child.draw_all()
            
    def set_all(self, var, val):
        self.__dict__[var] = val
        for child in self.children:
            child.set_all(var, val)
            
    def draw(self):
        pass
    
    def act_all(self):
        self.act()
        for child in self.children:
            child.act_all()
            
    def act(self):
        pass
    
    def input_all(self, events):
        self.input(events)
        for child in self.children:
            child.input_all(events)
            
    def input(self, events):
        pass
        
    def click_check(self, events):
        if self.rect is None:
            return False
        for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    if game.screen.scale_rect(self.rect).collidepoint(pygame.mouse.get_pos()):
                        self.clicked_on()
                        
    def clicked_on(self):
        pass
        