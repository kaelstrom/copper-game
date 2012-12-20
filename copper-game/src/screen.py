import pygame
import game
import fx
import math

class Screen(object):
    def __init__(self):
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((600,600))
        self.res = self.screen.get_rect()
        self.default_font = game.font_arial
        self.dimmer = pygame.Surface(self.screen.get_size())
        self.dimmer.fill((0,0,0))
        
    def blit(self, surf, rect, plasma=False):
        disp_rect = self.scale_rect(rect)
        disp_surf = pygame.transform.scale(surf, (disp_rect.width, disp_rect.height))
        if plasma:
            self.colorize_surf(disp_surf, disp_rect)
        self.screen.blit(disp_surf, disp_rect)
    
    def draw_text(self, text="", rect=pygame.Rect(0,0,1000,1000), font = None, scaling = False, color = (150,150,150), plasma=False):
        if font is None:
            font = self.default_font    
        disp_surf = font.render(text,1,color)
        #disp_rect = self.scale_rect(disp_surf.get_rect().move(rect.x, rect.y))
        disp_rect = self.scale_rect(rect)
        if plasma:
            shift = 6*(.5-math.sin(pygame.time.get_ticks()/100))
            disp_rect.width += shift
            disp_rect.height += shift
            disp_rect.x -= (shift/2)
            disp_rect.y -= (shift/2)
            if scaling:
                disp_surf = pygame.transform.scale(disp_surf, (disp_rect.width, disp_rect.height))
        elif scaling:
            #scale = min(disp_rect.width/disp_surf.get_rect().width, disp_rect.height/disp_surf.get_rect().height)
            scale = disp_rect.height/disp_surf.get_rect().height
            disp_surf = pygame.transform.scale(disp_surf, (disp_surf.get_rect().width*scale, disp_surf.get_rect().height*scale))
        if plasma:
            self.colorize_surf(disp_surf, disp_rect)
        self.screen.blit(disp_surf,disp_rect)
       
    def draw_line(self, a, b, color=(30,30,240), width=1):
        a_point = self.scale_rect(pygame.Rect(a, (0,0))).topleft
        b_point = self.scale_rect(pygame.Rect(b, (0,0))).topleft
        pygame.draw.line(self.screen, color, a_point, b_point, width)
        
    def get_text_rect(self, text="", font = None, color = (150,150,150), plasma=False):
        if font is None:
            font = self.default_font    
        disp_surf = font.render(text,1,color)
        return self.scale_rect(disp_surf.get_rect())
        
    def draw_outline(self, rect, color=(200,200,200), width=4):
        disp_rect = self.scale_rect(rect)
        pygame.draw.rect(self.screen, color, disp_rect, width)
        
    def scale_rect(self, rect):
        new_rect = rect.copy()
        new_rect.width = self.res.width*.001*rect.width
        new_rect.height = self.res.height*.001*rect.height
        new_rect.topleft = (rect.x*self.res.width*.001, rect.y*self.res.height*.001)
        return new_rect
        
    def colorize_surf(self, surf, rect):
        orig_alphas = pygame.surfarray.array_alpha(surf)
        plasma = fx.plasma
        surf.blit(plasma, (0,0), rect)
        alphas = pygame.surfarray.pixels_alpha(surf)
        alphas[:] = orig_alphas
        
        ''' super laggy solution
        surf.lock()
        for x in range(surf.get_rect().width):
            for y in range(surf.get_rect().height):
                c = surf.get_at((x,y))
                surf.set_at((x,y), (c[0], c[1], c[2], alphas[x][y]))
        surf.unlock()
        '''
        
    def dim(self, val=200):
        self.dimmer.set_alpha(val)
        self.screen.blit(self.dimmer,(0,0))
        
    def clear(self):
        self.screen.fill((0,0,0))
