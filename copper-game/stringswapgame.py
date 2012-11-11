'''
Created on Oct 7, 2012

@author: kaelstrom
'''

import game
import pygame
import screen
import node
import sound
import uservaluenode
import random
import string

class SwapLetter(node.Node):
    def __init__(self, letter, rect):
        super(SwapLetter, self).__init__()
        self.rect = rect
        self.set_letter(letter)
        
    def set_letter(self, letter):
        self.letter = self.key = letter
        if self.letter == ' ':
            self.letter = 'Spc'
        self.letter = self.letter + ' '
        self.surf = game.font_tempesta.render(self.letter,1,(200,200,200))
        
    def draw(self):
        game.screen.blit(self.surf, self.rect, plasma=True)
        
class LetterPair(node.Node):
    def __init__(self, lft, rht, rect, speed, delay, threshold):
        super(LetterPair, self).__init__()
        self.threshold = threshold
        self.lft = lft
        self.rht = rht
        self.children.append(self.lft)
        self.children.append(self.rht)
        if self.rht.key == ' ':
            self.rht.rect.x = self.rht.rect.x - self.rht.rect.width*.2
        self.progress = 0
        self.success = False
        self.failure = False
        self.top = lft.rect.y
        self.bottom = rht.rect.y
        self.dist = self.bottom - self.top
        self.speed = speed
        self.delay = delay
        self.rect = rect
        self.active = False
        self.cback_waiting = True
        self.rht_hit = False
        self.lft_hit = False
        self.getting_input = False
        
    def move(self, cback):
        if self.active and not self.failure:
            self.progress += self.speed * game.dt
            if self.progress >= 1:
                self.progress = 1
                self.active = False
            self.lft.rect.y = self.top + self.dist*self.progress
            self.rht.rect.y = self.bottom - self.dist*self.progress
            if self.progress >= self.delay and self.cback_waiting:
                self.cback_waiting = False
                cback()
                
    def act(self):
        if self.active and self.progress <= .5 + self.threshold and self.progress >= .5 - self.threshold:
            if not self.getting_input:
                global current_game
                current_game.play_chime()
            self.getting_input = True
            
        else:
            self.getting_input = False
            
        
        if not self.failure and not self.success and self.progress > .5 + self.threshold:
            self.failure = True
            r = random.choice(string.punctuation)
            self.parent.result_text += r
            self.lft.set_letter(r)
            self.rht.set_letter(r)
            sound.play_sound('fail.ogg')
                
    def draw_bg(self):
        #if self.active:
        #    game.screen.draw_outline(self.rect, (50,50,50), 0)
        if self.getting_input:
            game.screen.draw_outline(self.rect, (0,0,80), 0)
        if self.success:
            game.screen.draw_outline(self.rect, (0,80,0), 0)
        elif self.failure:
            game.screen.draw_outline(self.rect, (80,0,0), 0)
                
    def input(self, events):
        if self.getting_input:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.unicode == self.lft.key:
                        self.lft_hit = True
                    if e.unicode == self.rht.key:
                        self.rht_hit = True
                    if self.rht_hit and self.lft_hit:
                        if not self.success:
                            global current_game
                            current_game.success_count += 1
                            self.parent.result_text += self.rht.key
                        self.success = True
        
current_game = None
class StringSwapGame(node.Node):
    '''
    classdocs
    '''


    def __init__(self, start="", end="", cback=None, rect=pygame.Rect(100,300,800,400), speed=.0003, delay=.25, threshold = .07):
        '''
        Constructor
        '''
        super(StringSwapGame, self).__init__()
        global current_game
        current_game = self
        self.result_text = ''
        self.success_count = 0
        self.paused = True
        self.speed = speed
        self.delay = delay
        self.threshold = threshold
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
            lft = SwapLetter(s,pygame.Rect((i*2+0.2)*width+x,y,               width,width*1.5))
            rht = SwapLetter(e,pygame.Rect((i*2+1.2)*width+x,y+height-width*2,width,width*1.5))
            draw_rect = pygame.Rect((i*2)*width+x-width*.1,y,2*width,height)
            lpair = LetterPair(lft, rht, draw_rect, self.speed, self.delay, self.threshold)
            lpair.parent = self
            self.swaplist.append( lpair )
            self.draw_rects.append(draw_rect)
        
        for s in self.swaplist:
            self.children.append(s)
        
        self.rect.width = self.rect.width - width*.1
        self.hit_rect.width = self.hit_rect.width - width*.1
        self.rect.x = self.rect.x - width*.1
        self.hit_rect.x = self.hit_rect.x - width*.1
        
    def act(self):
        if self.cback is not None:
            for s in self.swaplist:
                if not (s.success or s.failure):
                    return
            self.cback()
        
    def next(self):
        self.swapindex = (self.swapindex + 1)%len(self.swaplist)
        if self.swapindex >= 0 and self.swapindex < len(self.swaplist):
            self.swaplist[self.swapindex].active = True
    
    def draw(self):
        for s in self.swaplist:
            s.draw_bg()
        for r in self.draw_rects:
            game.screen.draw_outline(r, (50,50,50), 2)
        game.screen.draw_outline(self.rect)
        game.screen.draw_outline(self.hit_rect)
    
   # def draw_all(self):
    #    self.draw()
     #   for p in self.swaplist:
      #      p.draw_all()
            
    def act_all(self):
        self.act()
        for s in self.swaplist:
            s.act()
            s.move(self.next)
            
    def input(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.paused:
                self.paused = False
                self.swaplist[0].active = True
                
    def play_chime(self):
        sound.play_sound("chime" + str( min(11, 1 + self.success_count) ) + ".ogg")
        
if __name__ == '__main__':
    game.init()
    game.screen = screen.Screen()
    ssg = StringSwapGame("cupcake", "toast n jam")
    ssg.act()
    ssg.draw()
        
