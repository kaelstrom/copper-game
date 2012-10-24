'''
Created on Sep 30, 2012

@author: kaelstrom
'''

import pygame
import game

class Screen(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((800,800))
        self.res = self.screen.get_rect()
        self.default_font = game.font_arial
        self.dimmer = pygame.Surface(self.screen.get_size())
        self.dimmer.fill((0,0,0))
        
    def blit(self, surf, rect):
        disp_rect = self.scale_rect(rect)
        disp_surf = pygame.transform.scale(surf, (disp_rect.width, disp_rect.height))
        self.screen.blit(disp_surf, disp_rect)
    
    def draw_text(self, text="", rect=pygame.Rect(0,0,1000,1000), font = None, scaling = False, color = (150,150,150)):
        if font is None:
            font = self.default_font    
        disp_surf = font.render(text,1,color)
        disp_rect = self.scale_rect(rect)
        if scaling:
            disp_surf = pygame.transform.scale(disp_surf, (disp_rect.width, disp_rect.height))
        self.screen.blit(disp_surf,disp_rect)
        
    def draw_outline(self, rect, color=(200,200,200), width=4):
        disp_rect = self.scale_rect(rect)
        pygame.draw.rect(self.screen, color, disp_rect, width)
        
    def scale_rect(self, rect):
        new_rect = rect.copy()
        new_rect.width = self.res.width*.001*rect.width
        new_rect.height = self.res.height*.001*rect.height
        new_rect.topleft = (rect.x*self.res.width*.001, rect.y*self.res.height*.001)
        return new_rect
        
    def dim(self, val=200):
        self.dimmer.set_alpha(val)
        self.screen.blit(self.dimmer,(0,0))
        
    def clear(self):
        self.screen.fill((0,0,0))
