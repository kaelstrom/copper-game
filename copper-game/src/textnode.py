import node
import pygame
import game

class TextNode(node.Node):
    def __init__(self, text="", rect=pygame.Rect(0,0,1000,1000)):
        super(TextNode, self).__init__()
        self.text = text
        self.rect = rect
        self.orig_rect= game.screen.get_text_rect(self.text)
        
        
    def draw(self):
        game.screen.draw_text(self.text, self.rect, scaling=self.scaling, plasma = self.plasma, depth = self.depth)
        #game.screen.draw_outline(self.orig_rect.move(self.rect.x, self.rect.y))
        
        