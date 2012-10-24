'''
Created on Sep 30, 2012

@author: kaelstrom
'''

import node
import pygame
import game
import stringswapgame
import stringnode

class ChoiceNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, text1=None, text2=None, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        super(ChoiceNode, self).__init__()
        self.rect = rect
        self.selection = 99
        self.choicemade = False
        self.gamerunning = False
        self.game = None
        self.mode = 'easy'
        if text1 is not None:
            self.children.append(stringnode.StringNode(text1, rect))
        if text2 is not None:
            self.children.append(stringnode.StringNode(text2, rect))
        
    def run_game(self):
        self.gamerunning = True
        if self.mode == 'hard':
            self.game = stringswapgame.StringSwapGame(self.children[0].text, self.children[1].text, cback=self.end_game, speed=.0003, delay=.25, threshold=.08)
        else:
            self.game = stringswapgame.StringSwapGame(self.children[0].text, self.children[1].text, cback=self.end_game, speed=.00035, delay=.5, threshold=.08)
        
        
    def end_game(self):
        self.choicemade = True
        self.gamerunning = False
        self.children[0], self.children[1] = self.children[1], self.children[0]
        
    def input_all(self, events):
        if self.gamerunning:
            self.game.input_all(events)
        if not self.choicemade and not self.gamerunning:
            for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    if game.screen.scale_rect(self.rect).collidepoint(pygame.mouse.get_pos()):
                        self.run_game()
        
    def act_all(self):
        if self.gamerunning:
            self.game.act_all()
        
        
    def draw_all(self):
        self.draw()
        if self.gamerunning or (not self.choicemade and game.screen.scale_rect(self.rect).collidepoint(pygame.mouse.get_pos())): 
            game.screen.draw_outline(self.rect.move(0,-self.rect.height/2), (0,0,0),0)
            game.screen.draw_outline(self.rect.move(0,-self.rect.height/2))
            game.screen.draw_outline(self.rect.move(0,self.rect.height/2), (0,0,0),0)
            game.screen.draw_outline(self.rect.move(0,self.rect.height/2))
            game.game.last_draw(self.draw_all)
            drawrect = self.rect.copy().move(10,-self.rect.height/2)
            for child in self.children:
                child.set_rect(drawrect)
                child.draw_all()
                drawrect.move_ip(0,self.rect.height)
        
        elif len(self.children) > 0:
            self.children[0].set_rect(self.rect.copy().move(10,0))
            self.children[0].draw_all()
            
        if self.gamerunning:
            game.game.last_draw(self.game_front)
            
    def game_front(self):
        game.screen.dim(200)
        self.game.draw_all()
            
    def draw(self):
        game.screen.draw_outline(self.rect.copy())
        if len(self.children) > self.selection:
            self.children[self.selection].draw_all()
