'''
Created on 2012 - 10 - 24

@author: kaelstrom
'''

import node
import textnode
import pygame
import choicenode

class EmailNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, text, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(EmailNode, self).__init__()
        self.generate(text, rect)
        
    def generate(self, text, rect):
        self.text = text
        self.rect = rect
        self.lines = self.text.split('\n')
        #spacing = 1.0/len(self.lines)
        spacing = 60
        self.disp_rect = self.rect.inflate(1, spacing/rect.height)
        self.children = []
        self.choicenodes = []
        for line in self.lines:
            if '{' not in line and '}' not in line:
                self.children.append(textnode.TextNode(line, self.disp_rect.copy()))
                self.disp_rect.move_ip(0,spacing)
            else:
                lft = line.split('{')[0]
                rht = line.split('{')[1].split('}')[1]
                a,b = line.split('{')[1].split('}')[0].split('|')
                line_edit = lft + ''.join(['  ' for i in range(max(len(a), len(b)) + 2)]) + rht
                self.children.append(textnode.TextNode(line_edit, self.disp_rect.copy()))
                choice_rect = self.disp_rect.copy()
                choice_rect.width = 24 * max(len(a), len(b))
                choice_rect.height = 60
                for i in lft:
                    choice_rect.move_ip(24,0)
                cnode = choicenode.ChoiceNode(a,b, choice_rect.copy())
                if len(a) <= 8:
                    cnode.mode = 'hard'
                self.choicenodes.append(cnode)
                    
                self.disp_rect.move_ip(0,spacing)
                
        self.choicenodes.reverse()
        for c in self.choicenodes:
            self.children.append(c)
