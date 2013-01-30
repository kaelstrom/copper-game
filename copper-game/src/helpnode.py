import node
import textnode
import pygame
import choicenode
import game
import uservaluenode
import scrollbox

class HelpNode(node.Node):
    def __init__(self, text="CONTINUE", 
                        rect=pygame.Rect(930,10,60,60),
                        depth=0):
        super(HelpNode, self).__init__()
        self.rect = rect
        self.text = text
        self.depth_adj = depth
        self.taking_input = True
        self.help_displayed = False
        self.surf = pygame.image.load('../res/unknown.png')
        self.help_rect = pygame.Rect(300,10,690,690)
        self.dimmer = pygame.Surface((self.rect.width+2, self.rect.height+2))
        self.dimmer.fill((0,0,0))
        self.generate()
        
    def input(self, events):
        if self.taking_input:
            for e in events:
                    if e.type == pygame.MOUSEBUTTONUP:
                        if game.screen.scale_rect(self.rect).collidepoint(pygame.mouse.get_pos()):
                            self.toggle_help()
                            
    def toggle_help(self):
        self.help_displayed = not self.help_displayed
                       
    def act(self):
        return
        self.fade += self.fade_rate * game.dt
        
        if self.fade > 1:
            self.taking_input = True
            self.fade = 1
            self.fade_rate = -self.fade_rate
        if self.fade_rate < 0 and self.fade < .8:
            self.fade_rate = -self.fade_rate
            
        self.dimmer.set_alpha(255-255*self.fade)
                        
    def draw(self):
        
        game.screen.draw_outline(self.rect, (150,150,150),depth=self.depth_adj+18)
        game.screen.blit(self.surf, self.rect,depth=self.depth_adj +17)
        if self.help_displayed:
            game.screen.draw_outline(self.help_rect, (30,30,30), width=0, depth = self.depth_adj+16)
            game.screen.draw_outline(self.help_rect, (150,150,150), width=1, depth = self.depth_adj+16.2)
            for s in self.scrollnodes:
                s.draw_all()
            
    def generate(self):
        self.lines = self.text.split('\n')
        
        for i in range(0,100):
            self.lines.append('')
        
        self.line_length = 32
            
        for i, line in enumerate(self.lines):
            while len(line) > self.line_length:
                index = line.rfind(' ')
                if index == -1:
                    self.lines[i+1] = line[self.line_length-1:].strip() + ' ' + self.lines[i+1].strip()
                    line = self.lines[i] = line[:self.line_length].strip()
                else:
                    self.lines[i+1] = line[index:].strip() + ' ' + self.lines[i+1].strip()
                    line = self.lines[i] = line[:index+1].strip()
                    
        while len(self.lines) > 0 and self.lines[-1].strip() is '':
            del self.lines[-1]
            
        #spacing = 1.0/len(self.lines)
        spacing = 60
        self.disp_rect = self.help_rect.move(10,0).inflate(1, spacing/self.help_rect.height)
        self.disp_rect.height = 60
        self.choicenodes = []
        self.scrollnodes = []
        c = 0
        for line in self.lines:
            if '{' not in line and '}' not in line:
                tmp = textnode.TextNode(line, self.disp_rect.copy())
                tmp.scaling=True
                self.scrollnodes.append(tmp)
                self.disp_rect.move_ip(0,spacing)
               

        for s in self.scrollnodes:
            s.set_all("depth", self.depth_adj+17)                        