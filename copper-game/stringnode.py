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
        lines = text.split('\n')
        disp_rect = rect.inflate(1, 1.0/len(lines))
        print rect
        print disp_rect
        print "lines: " + str(len(lines))
        for line in lines:
            self.children.append(textnode.TextNode(line, disp_rect.copy()))
            disp_rect.move_ip(0,rect.height/len(lines))
        