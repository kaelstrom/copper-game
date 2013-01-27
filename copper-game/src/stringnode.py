import node
import textnode
import pygame

class StringNode(node.Node):
    def __init__(self, text, rect=pygame.Rect(0,0,1000,1000), scrollbox=False):
        super(StringNode, self).__init__()
        self.text = text
        self.rect = rect
        self.scrollbox = scrollbox
        self.set_rect(self.rect)
        
    def set_rect(self, rect):
        self.rect = rect
        self.lines = self.text.split('\n')
        self.disp_rect = self.rect.inflate(1, 1.0/len(self.lines))
        self.children = []
        for line in self.lines:
            self.add(textnode.TextNode(line, self.disp_rect.copy()))
            self.disp_rect.move_ip(0,rect.height/len(self.lines))
        self.set_all('plasma', self.plasma)
