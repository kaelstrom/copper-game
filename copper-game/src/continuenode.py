import node
import textnode
import pygame
import choicenode
import game
import uservaluenode

class ContinueNode(node.Node):
    def __init__(self, rect=pygame.Rect(700,800,240,60)):
        super(ContinueNode, self).__init__()
        self.rect = rect
        
    def input(self, events):
        for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    if game.screen.scale_rect(self.rect).collidepoint(pygame.mouse.get_pos()):
                        self.next_scene()
                        
    def draw(self):
        game.screen.draw_outline(self.rect, (20,20,20),0)
        game.screen.draw_outline(self.rect, (150,150,150))
        game.screen.draw_text("CONTINUE", self.rect.move(25,0), scaling=True, plasma=False)
                        
    def next_scene(self):
        game.scriptmanager.next_scene()