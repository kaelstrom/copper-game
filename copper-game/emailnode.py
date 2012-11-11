'''
Created on 2012 - 10 - 24

@author: kaelstrom
'''

import node
import textnode
import pygame
import choicenode
import game
import uservaluenode

class EmailNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, text, vals, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(EmailNode, self).__init__()
        self.teenvalue = None
        if game.teenvalue is not None:
            self.teenvalue = game.teenvalue
        elif game.teen is not None:
            self.teenvalue = (uservaluenode.make_user(game.teen))
            game.teenvalue = self.teenvalue
        self.vals = vals
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
        c = 0
        for line in self.lines:
            if '{' not in line and '}' not in line:
                self.add(textnode.TextNode(line, self.disp_rect.copy()))
                self.disp_rect.move_ip(0,spacing)
            else:
                lft = line.split('{')[0]
                rht = line.split('{')[1].split('}')[1]
                a,b = line.split('{')[1].split('}')[0].split('|')
                line_edit = lft + ''.join(['  ' for i in range(max(len(a), len(b)) + 2)]) + rht
                tmp = textnode.TextNode(line_edit, self.disp_rect.copy())
                self.add(tmp)
                choice_rect = self.disp_rect.copy()
                choice_rect.width = 20 * max(len(a), len(b))
                choice_rect.height = 60
                #choice_rect.x = tmp.orig_rect.right
                for i in lft:
                   choice_rect.move_ip(20,0)
                cnode = choicenode.ChoiceNode(a,b, vals=self.vals[c], rect=choice_rect.copy())
                if len(a) <= 8:
                    cnode.mode = 'hard'
                if line != '\n':
                    self.choicenodes.append(cnode)
                c+=1
                self.disp_rect.move_ip(0,spacing)
                
        self.choicenodes.reverse()
        for c in self.choicenodes:
            self.add(c)



def test_email():
        return EmailNode(
            "From: investnews@consumerbuy.com\n" +
            "  Commercial property has been\n" +
            "  doing well for a while, and it\n" +
            "  appears the {residential|automotive}market \n" +
            "  is now following.{Sellers|Buyers} have \n" +
            "  a big chance to profit soon.",
            [[[0,0,0],[3,0,0]],[[-2,0,0],[4,0,2]]],
            pygame.Rect(100,100,800,800))