'''
Created on Sep 30, 2012

@author: kaelstrom
'''
import node
import pygame
import game

class TextNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, text="", rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(TextNode, self).__init__()
        self.text = text
        self.rect = rect
        
    def draw(self):
        game.screen.draw_text(self.text, self.rect)
        
        