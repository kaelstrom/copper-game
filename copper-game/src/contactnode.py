import node
import pygame
import game

class ContactNode(node.Node):

    def __init__(self, rect=pygame.Rect(0,0,1000,1000)):
        super(ContactNode, self).__init__()
        self.rect = rect
        self.name = "unknown"
        self.age = ""
        self.email = "root@localhost"
        self.phone = ""
        self.profile1 = ""
        self.profile2 = ""
        self.image = pygame.image.load("../res/unknown.png")
        
    def draw(self):
        game.screen.draw_outline(pygame.Rect(100,100,800,800), color = (30,30,30), width=0)
        game.screen.draw_outline(pygame.Rect(100,100,800,800))
        if self.image is not None:
            game.screen.blit(self.image, pygame.Rect(150,150,300,300))
        textcolor = (200,200,200)
        game.screen.draw_text("Name  : " + self.name,  pygame.Rect(500,150, 300,50), game.font_tempesta, True, textcolor)
        game.screen.draw_text("Age   : " + self.age,   pygame.Rect(500,250, 200,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Email : " + self.email, pygame.Rect(500,350, 300,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Phone : " + self.phone, pygame.Rect(500,450, 300,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("Profile : " + self.profile1, pygame.Rect(200,600, 600,50), game.font_tempesta, True,textcolor)
        game.screen.draw_text("          " + self.profile2, pygame.Rect(200,700, 600,50), game.font_tempesta, True,textcolor)
        
    def load_image(self, img):
        #print 'loading ../res/' + img
        self.image = pygame.image.load("../res/" + img)
        
def make_teen():
    tmp = ContactNode()
    tmp.name = "TBD"
    tmp.age = "18"
    tmp.email = "user@gmail.com"
    tmp.phone = "555-1234"
    tmp.image = pygame.image.load("../res/john.png")
    return tmp