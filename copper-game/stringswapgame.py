'''
Created on Oct 7, 2012

@author: kaelstrom
'''

import game
import pygame
import screen

class SwapLetter(object):
    def __init__(self, letter, rect):
        self.letter = letter
        self.rect = rect
        self.surf = game.font_tempesta.render(letter,0,(200,200,200))
        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))
        
    def draw(self):
        game.screen.blit(self.surf, self.rect)

class StringSwapGame(object):
    '''
    classdocs
    '''


    def __init__(self, start="", end="", cback=None, rect=pygame.Rect(0,0,1000,1000)):
        '''
        Constructor
        '''
        self.start = start
        self.end = end
        self.cback = cback
        self.swaplist = []
        self.swapindex = 0
        self.rect = rect
        x = self.rect.x
        y = self.rect.y
        height = self.rect.height
        width = self.rect.width / (2*max(len(start), len(end)))
        for i in range(max(len(start), len(end))):
            if i < len(start): 
                s = start[i]
            else: 
                s = ' '
            if i < len(end): 
                e = end[i]
            else: 
                e = ' '
            if s != e:
                self.swaplist.append(
                    [SwapLetter(s,pygame.Rect((i*2  )*width+x,y,               width,width*1.5)),
                     SwapLetter(e,pygame.Rect((i*2+1)*width+x,y+height-width*2,width,width*1.5))])
        
        
    def act(self):
        pass
    
    def draw(self):
        pass
    
    def draw_all(self):
        for p in self.swaplist:
            p[0].draw()
            p[1].draw()
        
        
if __name__ == '__main__':
    game.init()
    game.screen = screen.Screen()
    ssg = StringSwapGame("cupcake", "toast n jam")
    ssg.act()
    ssg.draw()
        