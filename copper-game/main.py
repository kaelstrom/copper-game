'''
Created on Sep 29, 2012

@author: kaelstrom
'''

import screen
import node
import stringnode
import textnode
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
        pygame.init()
        self.screen = screen.Screen()
        self.clock = pygame.time.Clock()
        self.dt = 0
        test = node.Node()
        c = choicenode.ChoiceNode(pygame.Rect(50,50,300,300))
        c.add(stringnode.StringNode("test\n chunk one\ntest\ntest", pygame.Rect(000,200,800,800)))
        test.add(c)
        test.add(stringnode.StringNode("test chunk 2\nLorem Ipsum", pygame.Rect(500,500,500,200)))
        self.active_node = test
    
    def start(self):
        self.main_loop()
        
    def main_loop(self):
        self.running = True
        while(self.running):
            self.dt = self.clock.tick(60)
            self.input()
            self.act()
            self.draw()
        
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def act(self):
        pass
    
    def draw(self):
        self.screen.clear()
        self.active_node.draw_all()
        pygame.display.flip()
    
if __name__ == '__main__':
    g = Game()
    game.game = g
    game.screen = g.screen
    g.start()