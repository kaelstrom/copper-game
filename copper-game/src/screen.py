import pygame
import game
import fx
import math
import copy

class Screen(object):
    def __init__(self):
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.size = 800, 800
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.res = self.screen.get_rect()
        self.default_font = game.font_arial
        self.dimmer = pygame.Surface(self.screen.get_size())
        self.dimmer.fill((0,0,0))
        self.draw_calls = []
        self.depth_offset = 0
        self.depth_inc = .00001
        
        
    def blit(self, surf, rect, plasma=False, centered=False, depth=0):
        args = (surf.copy(), rect.copy(), plasma, centered)
        self.queue_draw(self.blit_real, args, depth)
        
    def blit_real(self, args):
        surf=args[0]
        rect= args[1]
        plasma=args[2]
        centered=args[3]
        disp_rect = self.scale_rect(rect)
        disp_surf = pygame.transform.scale(surf, (disp_rect.width, disp_rect.height))
        if plasma:
            self.colorize_surf(disp_surf, disp_rect)
        if centered:
            disp_rect.move_ip(-(disp_surf.get_rect().width - disp_rect.width)/2,0)
        self.screen.blit(disp_surf, disp_rect)
    
    def draw_text(self, text="", rect=pygame.Rect(0,0,1000,1000), font = None, scaling = False, color = (150,150,150), plasma=False, centered=False, depth=0):
        args = (text, rect.copy(), font, scaling, color, plasma, centered)
        self.queue_draw(self.draw_text_real, args, depth)
    
    def draw_text_real(self, args):
        text=args[0]
        rect=args[1]
        font=args[2]
        scaling=args[3]
        color=args[4]
        plasma=args[5]
        centered=args[6]
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
        if centered:
            disp_rect.move_ip(-(disp_surf.get_rect().width - disp_rect.width)/2,0)
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
     
    def draw_outline(self, rect, color=(200,200,200), width=4, depth=0):
        args = (rect.copy(), color, width)
        self.queue_draw(self.draw_outline_real, args, depth)
        
    def draw_outline_real(self, args):
        rect=args[0]
        color=args[1]
        width=args[2]
        disp_rect = self.scale_rect(rect)
        pygame.draw.rect(self.screen, color, disp_rect, width)
        
    def resize(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        tmp_res = self.screen.get_rect()
        self.res = tmp_res.copy()
        self.res.height = self.res.width = min(tmp_res.height, tmp_res.width)
        self.res.center = tmp_res.center
        
    
    def scale_rect(self, rect):
        new_rect = rect.copy()
        new_rect.width = self.res.width*.001*rect.width
        new_rect.height = self.res.height*.001*rect.height
        new_rect.topleft = (rect.x*self.res.width*.001+self.res.x, rect.y*self.res.height*.001+self.res.y)
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
        
    def queue_draw(self, func, args, depth):
        self.depth_offset += self.depth_inc
        self.draw_calls.append((depth+self.depth_offset, func, args))
        
    def expel_draw_queue(self):
        
        self.draw_calls.sort(key=lambda x: x[0])
                
        for call in self.draw_calls:
            call[1](call[2])
            
            
        self.depth_offset = 0
        self.draw_calls = []
        
    def dim(self, val=200, depth=5):
        args = (val)
        self.queue_draw(self.dim_real, args, depth)
        
    def dim_real(self, args):
        val = args
        self.dimmer.set_alpha(val)
        self.screen.blit(self.dimmer,(0,0))
        
    def clear(self):
        self.screen.fill((0,0,0))
