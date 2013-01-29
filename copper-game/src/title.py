import node
import pygame
import game
import random
import string
import copy
import commentgame
import continuenode

class Title(node.Node):
    def __init__(self, text="", rect=pygame.Rect(0,0,1000,1000)):
        super(Title, self).__init__()
        self.rect = rect
        self.text = text
        self.swap_timers = [0,0,0,0,0,0]
        self.swap_caps = [9,9,9,9,9,9]
        self.timer_cap = 10
        self.text = 'copper'
        self.seed_surfs = []
        for i in self.text:
            self.seed_surfs.append(game.font_tempesta.render(i,0,(255,255,255)).convert_alpha())
        self.title_surfs = []
        for surf in self.seed_surfs:
            self.title_surfs.append(surf.convert_alpha())
        self.dimmer = pygame.Surface(self.title_surfs[0].get_size())
        self.dimmer.fill((0,0,0))
        self.dimmer.set_alpha(10)
        self.children.append(continuenode.ContinueNode("START", pygame.Rect(550, 50, 400, 160)))
        #self.children.append(commentgame.CommentGame('title'))
        
    def draw(self):
        width = 900/len(self.title_surfs)
        for i, surf in enumerate(self.title_surfs):
            game.screen.blit(surf, pygame.Rect((i+.2)*width,0,width,1000), depth=-5)
        
    def act(self):
        for i in range(len(self.swap_caps)):
            self.swap_caps[i] += random.uniform(.001,.005) * game.dt + ((7-i)*.03)
            self.swap_timers[i] += random.uniform(.1,.2) * game.dt
            if self.swap_timers[i] >= self.swap_caps[i]:
                self.swap_timers[i] = 0
                if self.swap_caps[i] > 60:
                    self.text = self.text[:i] + 'copper'[i] + self.text[i+1:]
                else:
                    self.text = self.text[:i] + random.choice(string.lowercase) + self.text[i+1:]
        
        for i, t in enumerate(self.text):
            self.seed_surfs[i] = game.font_tempesta.render(t,0,(255,255,255)).convert_alpha() 
        for i, surf in enumerate(self.seed_surfs):
            self.title_surfs[i].blit(self.dimmer, (0,0))
            self.title_surfs[i].blit(surf, (0,0))