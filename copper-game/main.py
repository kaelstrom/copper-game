'''
Created on Sep 29, 2012

@author: kaelstrom
'''

import screen
import node
import stringnode
import textnode
import stringswapgame
import choicenode
import contactnode
import emailnode
import pygame
import game

class Game(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.running = False
        game.init()
        self.screen = screen.Screen()
        self.clock = pygame.time.Clock()
        self.scene_num = 0
        self.scenes = []
        self.ldraw = None
        self.activescenestack = []
        self.teen = contactnode.make_teen()
        game.teen = self.teen
        #test = node.Node()
        #test.add(stringswapgame.StringSwapGame("cupcake", "expensive", speed=.0003, delay=.25, threshold=.08))
        #self.scenes.append(test)
        
        self.scenes.append(emailnode.EmailNode(
            "From: investnews@consumerbuy.com\n" +
            "  Commercial property has been\n" +
            "  doing well for a while, and it\n" +
            "  appears the {residential|automotive}market \n" +
            "  is now following.{Sellers|Buyers} have \n" +
            "  a big chance to profit soon. \n",
            [[[0,0,0],[3,0,0]],[[-2,0,0],[4,0,2]]],
            pygame.Rect(100,100,800,800)))
        
        self.scenes.append(self.teen)
        
        #c = choicenode.ChoiceNode(pygame.Rect(50,50,300,100))
        #c.add(stringnode.StringNode("testing", pygame.Rect(050,050,300,100)))
        #c.add(stringnode.StringNode("results", pygame.Rect(150,050,300,100)))
        #self.scenes.append(c)
        
        self.active_node = self.scenes[self.scene_num]
    
    def start(self):
        self.main_loop()
        
    def main_loop(self):
        self.running = True
        while(self.running):
            game.dt = self.clock.tick(60)
            self.input()
            self.act()
            self.draw()
        
    def input(self):
        events = pygame.event.get() 
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.scene_num = (self.scene_num + 1) % len(self.scenes)
                    self.active_node = self.scenes[self.scene_num]
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        self.active_node.input_all(events)
                    
    def act(self):
        self.active_node.act_all()
    
    def draw(self):
        self.screen.clear()
        self.active_node.draw_all()
        if self.ldraw is not None:
			self.ldraw()
			self.ldraw = None
        pygame.display.flip()
        
    def last_draw(self, func):
		self.ldraw = func
		
    
if __name__ == '__main__':
    g = Game()
    game.game = g
    game.screen = g.screen
    g.start()
