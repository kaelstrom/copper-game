'''
Created on Oct 30, 2012

@author: kaelstrom
'''
import node
import pygame
import game

class UserValueNode(node.Node):
    def __init__(self, rect=pygame.Rect(20,720,380,260)):
        super(UserValueNode, self).__init__()
        self.rect = rect
        self.picture = None
        self.spending = 15
        self.political = 40
        self.suspicion = 5
        
    def draw(self):
        game.screen.draw_outline(self.rect, color = (30,30,30), width=0)
        game.screen.draw_outline(self.rect)
        if self.picture is not None:
            game.screen.blit(self.picture, pygame.Rect(50,800,100,100))
        
        textcolor = (200,200,200)
        game.screen.draw_text("Spending : " + str(self.spending),  pygame.Rect(180,740, 120,40), game.font_tempesta, True, textcolor)
        game.screen.draw_text("Political: " + str(self.political),    pygame.Rect(180,810, 120,40), game.font_tempesta, True, textcolor)
        game.screen.draw_text("Suspicion: " + str(self.suspicion),  pygame.Rect(180,880, 120,40), game.font_tempesta, True, textcolor)
        
        game.screen.draw_outline(pygame.Rect(180,775, 2*self.spending,30), color=(0,250,0), width=0)
        game.screen.draw_outline(pygame.Rect(180,845, 2*self.political,30), color=(0,0,250), width=0)
        game.screen.draw_outline(pygame.Rect(180,915, 2*self.suspicion,30), color=(250,0,0), width=0)
        
        game.screen.draw_outline(pygame.Rect(180,775, 200,30))
        game.screen.draw_outline(pygame.Rect(180,845, 200,30))
        game.screen.draw_outline(pygame.Rect(180,915, 200,30))
        
    def add(self, vals):
        self.spending += vals[0]
        self.political += vals[1]
        self.suspicion += vals[2]       
        
def make_user(contact):
    tmp = UserValueNode()
    tmp.picture = contact.picture
    return tmp