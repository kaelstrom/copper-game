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
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.res = self.screen.get_rect()
        self.default_font = pygame.font.SysFont("arial", 48)
        
    
    def draw_text(self, text="", font=None, pos=(.5,.5)):
        if font is None:
            font = self.default_font
        self.screen.blit(font.render(text,1,(150,150,150)),(pos[0]*self.res.width, pos[1]*self.res.height))
        
    def clear(self):
        self.screen.fill((0,0,0))