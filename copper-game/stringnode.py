'''
Created on Sep 30, 2012

@author: kaelstrom
'''

import node
import textnode
import pygame

class StringNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, text, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(StringNode, self).__init__()
        self.text = text
        self.rect = rect
        
        self.set_rect(self.rect)
        
    def set_rect(self, rect):
        self.rect = rect
        self.lines = self.text.split('\n')
        self.disp_rect = self.rect.inflate(1, 1.0/len(self.lines))
        self.children = []
        for line in self.lines:
            self.children.append(textnode.TextNode(line, self.disp_rect.copy()))
            self.disp_rect.move_ip(0,rect.height/len(self.lines))
        
