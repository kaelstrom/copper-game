'''
Created on Oct 17, 2012

@author: kaelstrom
'''
import node
import pygame
import game

class ContactNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(ContactNode, self).__init__()
        self.rect = rect
        self.name = ""
        self.age = ""
        self.email = ""
        self.phone = ""
        self.picture = None
        self.profile1 = ""
        self.profile2 = ""
        
        
    def draw(self):
        game.screen.draw_outline(pygame.Rect(100,100,800,800), color = (30,30,30), width=0)
        game.screen.draw_outline(pygame.Rect(100,100,800,800))
        if self.picture is not None:
            game.screen.blit(self.picture, pygame.Rect(150,150,300,300))
        textcolor = (200,200,200)
        game.screen.draw_text("Name  : " + self.name,  pygame.Rect(500,150, 300,50), game.font_tempesta, True, textcolor)
        game.screen.draw_text("Age   : " + self.age,   pygame.Rect(500,250, 200,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Email : " + self.email, pygame.Rect(500,350, 300,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Phone : " + self.phone, pygame.Rect(500,450, 300,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Profile : " + self.profile1, pygame.Rect(200,600, 600,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("          " + self.profile2, pygame.Rect(200,700, 600,50), game.font_tempesta, True,textcolor)
        
def make_teen():
    tmp = ContactNode()
    tmp.name = "TBD"
    tmp.age = "18"
    tmp.email = "user@gmail.com"
    tmp.phone = "555-1234"
    tmp.picture = pygame.image.load("teen.png")
    tmp.profile1 = "high school senior, emotionally naive"
    tmp.profile2 = "child of congressional candidate"
    return tmp