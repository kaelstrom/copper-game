import node
import textnode
import pygame
import choicenode
import game
import uservaluenode

class ContinueNode(node.Node):
    def __init__(self, text="CONTINUE", 
                        rect=pygame.Rect(700,800,240,60),
                        callback=None):
        super(ContinueNode, self).__init__()
        self.rect = rect
        self.text = text
        if callback is None:
            self.callback = game.scriptmanager.next_scene
        else:
            self.callback = callback
        self.fade = .3
        self.fade_rate = .001
        self.taking_input = True
        self.dimmer = pygame.Surface((self.rect.width+2, self.rect.height+2))
        self.dimmer.fill((0,0,0))
        
    def input(self, events):
        if self.taking_input:
            for e in events:
                    if e.type == pygame.MOUSEBUTTONUP:
                        if game.screen.scale_rect(self.rect).collidepoint(pygame.mouse.get_pos()):
                            self.callback()
                       
    def act(self):
        self.fade += self.fade_rate * game.dt
        
        if self.fade > 1:
            self.taking_input = True
            self.fade = 1
            self.fade_rate = -self.fade_rate
        if self.fade_rate < 0 and self.fade < .8:
            self.fade_rate = -self.fade_rate
            
        self.dimmer.set_alpha(255-255*self.fade)
                        
    def draw(self):
        game.screen.draw_outline(self.rect, (20,20,20),0, depth=0)
        game.screen.draw_outline(self.rect, (150,150,150),depth=0)
        game.screen.draw_text(self.text, self.rect, scaling=True, plasma=False, centered=True,depth=1)
        game.screen.blit(self.dimmer, self.rect.inflate(1,1), depth = 2)
                        