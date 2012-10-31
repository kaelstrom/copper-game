'''
Created on Oct 30, 2012

@author: kaelstrom
'''
import node
import pygame
import game

class UserValueNode(node.Node):
    def __init__(self, rect=pygame.Rect(600,0,400,300)):
        super(ContactNode, self).__init__()
        self.rect = rect
        self.picture = None
        
    def draw(self):
        game.screen.draw_outline(self.rect, color = (30,30,30), width=0)
        game.screen.draw_outline(self.rect)
        if self.picture is not None:
            game.screen.blit(self.picture, pygame.Rect(850,100,100,100))
        '''
        textcolor = (200,200,200)
        game.screen.draw_text("Name  : " + self.name,  pygame.Rect(500,150, 300,50), game.font_tempesta, True, textcolor)
        game.screen.draw_text("Age   : " + self.age,   pygame.Rect(500,250, 200,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Email : " + self.email, pygame.Rect(500,350, 300,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Phone : " + self.phone, pygame.Rect(500,450, 300,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Profile : " + self.profile1, pygame.Rect(200,600, 600,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("          " + self.profile2, pygame.Rect(200,700, 600,50), game.font_tempesta, True,textcolor)
        '''
        
def make_user(contact):
    tmp = UserValueNode()
    tmp.picture = contact.picture
    return tmp