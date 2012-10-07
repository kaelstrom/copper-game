'''
Created on Sep 30, 2012

@author: kaelstrom
'''

import node
import pygame
import game

class ChoiceNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(ChoiceNode, self).__init__()
        self.rect = rect
        self.selection = 99
        
    def draw_all(self):
        self.draw()
        if self.rect.collidepoint(pygame.mouse.get_pos()):   
            for child in self.children:
                child.draw_all()
            
    def draw(self):
        game.screen.draw_outline(self.rect)
        if len(self.children) > self.selection:
            self.children[self.selection].draw_all()