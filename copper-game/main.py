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
        test = node.Node()
        test.add(stringswapgame.StringSwapGame("limited sale", "expensive", speed=.0004, delay=.5, threshold=.08))
        '''
        c = choicenode.ChoiceNode(pygame.Rect(50,50,300,300))
        c.add(stringnode.StringNode("test\n chunk one\ntest\ntest", pygame.Rect(000,200,800,800)))
        test.add(c)
        test.add(stringnode.StringNode("test chunk 2\nLorem Ipsum", pygame.Rect(500,500,500,200)))
        '''
        self.active_node = test
    
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
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        self.active_node.input_all(events)
                    
    def act(self):
        self.active_node.act_all()
    
    def draw(self):
        self.screen.clear()
        self.active_node.draw_all()
        pygame.display.flip()
    
if __name__ == '__main__':
    g = Game()
    game.game = g
    game.screen = g.screen
    g.start()