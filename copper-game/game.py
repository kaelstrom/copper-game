'''
Created on Sep 29, 2012

@author: kaelstrom
'''

import screen
import node
import stringnode
import textnode
import pygame

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
        self.active_node = textnode.TextNode("oloasdla a waefwa")
    
    def start(self):
        print "Game start called"
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def act(self):
        pass
    
    def draw(self):
        self.screen.clear()
        self.active_node.draw_all()
        pygame.display.flip()
        
    
game = Game()
    
if __name__ == '__main__':
    game.start()