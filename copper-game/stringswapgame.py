'''
Created on Oct 7, 2012

@author: kaelstrom
'''

import game
import pygame
import screen
import node

class SwapLetter(node.Node):
    def __init__(self, letter, rect):
        super(SwapLetter, self).__init__()
        self.letter = self.key = letter
        if self.letter == ' ':
            self.letter = 'Spc'
        self.letter = self.letter + ' '
        self.rect = rect
        self.surf = game.font_tempesta.render(self.letter,0,(200,200,200))
        
    def draw(self):
        game.screen.blit(self.surf, self.rect)
        
class LetterPair(node.Node):
    def __init__(self, lft, rht, speed=.0004):
        super(LetterPair, self).__init__()
        self.lft = lft
        self.rht = rht
        self.children.append(self.lft)
        self.children.append(self.rht)
        if self.rht.key == ' ':
            self.rht.rect.x = self.rht.rect.x - self.rht.rect.width*.2
        self.progress = 0
        self.success = False
        self.top = lft.rect.y
        self.bottom = rht.rect.y
        self.dist = self.bottom - self.top
        self.speed = speed
        self.active = False
        self.cback_waiting = True
        
    def move(self, cback):
        if self.active:
            self.progress += self.speed * game.dt
            self.lft.rect.y = self.top + self.dist*self.progress
            self.rht.rect.y = self.bottom - self.dist*self.progress
            if self.progress >= .5 and self.cback_waiting:
                self.cback_waiting = False
                cback()
            if self.progress >= 1:
                self.progress = 1
                self.active = False
                
    def input(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                print e.key
        

class StringSwapGame(node.Node):
    '''
    classdocs
    '''


    def __init__(self, start="", end="", cback=None, rect=pygame.Rect(200,300,600,400)):
        '''
        Constructor
        '''
        super(StringSwapGame, self).__init__()
        self.start = start
        self.end = end
        self.cback = cback
        self.swaplist = []
        self.draw_rects = []
        self.swapindex = 0
        self.rect = rect
        self.hit_rect = self.rect.copy()
        self.hit_rect.height = self.hit_rect.height/8
        self.hit_rect.center = self.rect.center
        x = self.rect.x
        y = self.rect.y
        height = self.rect.height
        width = (self.rect.width-1) / (2*max(len(start), len(end)))
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
                self.swaplist.append( LetterPair(
                     SwapLetter(s,pygame.Rect((i*2+0.2)*width+x,y,               width,width*1.5)),
                     SwapLetter(e,pygame.Rect((i*2+1.2)*width+x,y+height-width*2,width,width*1.5))))
                self.draw_rects.append(pygame.Rect((i*2)*width+x-width*.1,y,2*width,height))
        
        for s in self.swaplist:
            self.children.append(s)
        
        self.rect.width = self.rect.width - width*.1
        self.hit_rect.width = self.hit_rect.width - width*.1
        self.rect.x = self.rect.x - width*.1
        self.hit_rect.x = self.hit_rect.x - width*.1
        self.swaplist[0].active = True
        
    def act(self):
        #if self.swapindex >= 0 and self.swapindex < len(self.swaplist):
        #    self.swaplist[self.swapindex].move(self.next)
        pass
        
    def next(self):
        self.swapindex += 1
        if self.swapindex >= 0 and self.swapindex < len(self.swaplist):
            self.swaplist[self.swapindex].active = True
        if self.swapindex > len(self.swaplist)-1 and self.cback is not None:
            self.cback()
    
    def draw(self):
        for r in self.draw_rects:
            game.screen.draw_outline(r, (50,50,50), 2)
        game.screen.draw_outline(self.rect)
        game.screen.draw_outline(self.hit_rect)
    
    def draw_all(self):
        self.draw()
        for p in self.swaplist:
            p.draw_all()
            
    def act_all(self):
        self.act()
        for s in self.swaplist:
            s.move(self.next)
        
        
if __name__ == '__main__':
    game.init()
    game.screen = screen.Screen()
    ssg = StringSwapGame("cupcake", "toast n jam")
    ssg.act()
    ssg.draw()
        