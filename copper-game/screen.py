'''
Created on Sep 30, 2012

@author: kaelstrom
'''

import pygame

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
        self.default_font = pygame.font.SysFont("arial", 48)
        
    
    def draw_text(self, text="", rect=pygame.Rect(0,0,1000,1000)):
        font = self.default_font    
        disp_surf = font.render(text,1,(150,150,150))
        disp_rect = self.scale_rect(rect)
        self.screen.blit(disp_surf,disp_rect)
        
    def draw_outline(self, rect):
        disp_rect = self.scale_rect(rect)
        pygame.draw.rect(self.screen, (200,200,200), disp_rect, 10)
        
    def scale_rect(self, rect):
        new_rect = rect.inflate(self.res.width*.001, self.res.height*.001)
        new_rect.topleft = (rect.x*self.res.width*.001, rect.y*self.res.height*.001)
        return new_rect
        
    def clear(self):
        self.screen.fill((0,0,0))