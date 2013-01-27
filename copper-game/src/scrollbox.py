import pygame
import screen
import game
import node
import textnode
import choicenode

class ScrollBox(node.Node):
    def __init__ (self):
        super(ScrollBox, self).__init__()
        self.text = ""
        self.rect = pygame.Rect(0,0,0,0)
        self.scrollnodes = []
        self.scroll = 0
        self.scrollincrement = 64
        self.scroll_bounds = (0,200)
        self.input_up = False
        self.input_down = False
        self.input_up_timer = 0
        self.input_down_timer = 0
        self.input_timer_threshold = 0
        self.input_up_held = False
        self.input_down_held = False
        self.hold_speed = .1
        self.scroll_enabled = False
        self.scroll_up_rect = None
        self.scroll_down_rect = None
        self.scroll_up_surf = None
        self.scroll_down_surf = None
        self.scroll_bar_rect = None
        
    def draw(self):
        game.screen.draw_outline(self.rect.inflate(24,24), (100,100,100), 4, depth=-8)
        game.screen.draw_outline(pygame.Rect(0,0,1000,self.rect.top), (0,0,0),0,depth=-9)
        game.screen.draw_outline(pygame.Rect(0,0,self.rect.left,1000), (0,0,0),0,depth=-9)
        game.screen.draw_outline(pygame.Rect(self.rect.right,0,1000,1000), (0,0,0),0,depth=-9)
        game.screen.draw_outline(pygame.Rect(0,self.rect.bottom,1000,1000), (0,0,0),0,depth=-9)
        
        if self.scroll_enabled:
            game.screen.blit(self.scroll_up_surf, self.scroll_up_rect, depth = -7)
            game.screen.blit(self.scroll_down_surf, self.scroll_down_rect, depth = -7)
            game.screen.draw_outline(self.scroll_bar_rect.move(0,2), color=(100,100,100), width=4, depth = -6)
            game.screen.draw_outline(self.scroll_bar_rect.move(0,2), color=(50,50,50), width=0, depth = -7)
        
        for s in self.scrollnodes:
            s.draw_all()
        
        #for s in self.scrollnodes:
        #    game.screen.draw_text(s.text, s.rect.move(0,-self.scroll), scaling=True, depth=-10)
       
    def create_scroll_bar(self, size = 32):
        print "self.rect.top" 
        print self.rect.top
        self.scroll_up_surf = pygame.image.load("../res/scroll_up.png")
        self.scroll_down_surf = pygame.transform.flip(self.scroll_up_surf, False, True)
        self.scroll_up_rect = pygame.Rect(self.rect.right-size,self.rect.top,size,size)
        self.scroll_down_rect = pygame.Rect(self.rect.right-size,self.rect.bottom-size,size,size)
        self.scroll_bar_rect = pygame.Rect( self.rect.right-size, self.rect.top+size, size, (self.scroll_down_rect.top - self.scroll_up_rect.bottom)/2)
        self.scroll_bar_dist = (self.scroll_down_rect.top - self.scroll_up_rect.bottom - self.scroll_bar_rect.height)
        
        
    def input(self, events):
        #combine up/down keypress and scroll arrows into single input variables
        if self.scroll_enabled:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.input_up = False
                    self.input_down = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        #self.move_scroll(-self.scrollincrement)
                        self.input_up = True
                    if event.key == pygame.K_DOWN:
                        #self.move_scroll(self.scrollincrement)
                        self.input_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.input_up = False
                    if event.key == pygame.K_DOWN:
                        self.input_down = False
        
            if pygame.mouse.get_pressed()[0] and game.screen.scale_rect(self.scroll_up_rect).collidepoint(pygame.mouse.get_pos()):
                self.input_up = True
            if pygame.mouse.get_pressed()[0] and game.screen.scale_rect(self.scroll_down_rect).collidepoint(pygame.mouse.get_pos()):
                self.input_down = True
            
        for s in self.scrollnodes:
            s.input_all(events)
        
    def act(self):
        
        #track if up is held
        if self.input_up:
            self.input_up_timer += 1 * game.dt
            if self.input_up_timer > self.input_timer_threshold:
                self.input_up_held = True
        else:
            self.input_up_held= False
            self.input_up_timer = 0
        
        #track is down is held
        if self.input_down:
            self.input_down_timer += 1 * game.dt
            if self.input_down_timer > self.input_timer_threshold:
                self.input_down_held = True
        else:
            self.input_down_held= False
            self.input_down_timer = 0
            
        #continue scrolling if up or down is held
        if self.input_up_held:
            self.move_scroll(-self.scrollincrement*self.hold_speed)
        if self.input_down_held:
            self.move_scroll(self.scrollincrement*self.hold_speed)
        
    def move_scroll(self, val):
        self.scroll = self.scroll + val
        if self.scroll < self.scroll_bounds[0]:
            val = val + (self.scroll_bounds[0] - self.scroll)
            self.scroll = self.scroll_bounds[0]
        if self.scroll > self.scroll_bounds[1]:
            val = val + (self.scroll_bounds[1] - self.scroll)
            self.scroll = self.scroll_bounds[1]
        for s in self.scrollnodes:
            s.rect.move_ip(0,-val)
        self.scroll_bar_rect.move_ip(0, self.scroll_bar_dist * (val / (self.scroll_bounds[1] - self.scroll_bounds[0])))
        
    def generate(self, text, vals, rect):

        self.text = text
        self.vals = vals
        self.rect = rect.copy()
        self.lines = self.text.split('\n')
        
        for i in range(0,100):
            self.lines.append('')
        
        self.line_length = 42
            
        for i, line in enumerate(self.lines):
            while len(line) > self.line_length:
                index = line.rfind(' ')
                if index == -1:
                    self.lines[i+1] = line[self.line_length-1:].strip() + ' ' + self.lines[i+1].strip()
                    line = self.lines[i] = line[:self.line_length].strip()
                else:
                    self.lines[i+1] = line[index:].strip() + ' ' + self.lines[i+1].strip()
                    line = self.lines[i] = line[:index+1].strip()
                    
        while len(self.lines) > 0 and self.lines[-1].strip() is '':
            del self.lines[-1]
            
        #spacing = 1.0/len(self.lines)
        spacing = 60
        self.disp_rect = self.rect.inflate(1, spacing/rect.height)
        self.disp_rect.height = 60
        self.choicenodes = []
        self.scrollnodes = []
        c = 0
        for line in self.lines:
            if '{' not in line and '}' not in line:
                tmp = textnode.TextNode(line, self.disp_rect.copy())
                tmp.scaling=True
                self.scrollnodes.append(tmp)
                self.disp_rect.move_ip(0,spacing)
            else:
                lft = line.split('{')[0]
                rht = line.split('{')[1].split('}')[1]
                try:
                    a,b = line.split('{')[1].split('}')[0].split('|')
                except:
                    a,b = line.split('{')[1].split('}')[0], ''
                line_edit = lft + ''.join(['  ' for i in range(max(len(a), len(b)) + 2)]) + rht
                tmp = textnode.TextNode(line_edit, self.disp_rect.copy())
                tmp.scaling=True
                self.scrollnodes.append(tmp)
                choice_rect = self.disp_rect.copy()
                choice_rect.width = 20 * max(len(a), len(b))
                choice_rect.height = 60
                #choice_rect.x = tmp.orig_rect.right
                for i in lft:
                   choice_rect.move_ip(20,0)
                cnode = choicenode.ChoiceNode(a,b, vals=self.vals[c], rect=choice_rect.copy())
                if len(a) <= 8:
                    cnode.mode = 'hard'
                if line != '\n':
                    self.choicenodes.append(cnode)
                c+=1
                self.disp_rect.move_ip(0,spacing)
                
        if (self.disp_rect.bottom - self.rect.top) - self.rect.height > 0:
            self.scroll_bounds = (0, (self.disp_rect.bottom - self.rect.top) - self.rect.height)
        else:
            self.scroll_bounds = (0,0)
            
        if self.scroll_bounds != (0,0):
            self.scroll_enabled = True
            self.create_scroll_bar()
        else:
            self.scroll_enabled = False
        
        self.choicenodes.reverse()
        for c in self.choicenodes:
            self.scrollnodes.append(c)
            
        for s in self.scrollnodes:
            s.set_all("depth", -10)