import node
import game
import pygame
import screen
import random
import math
import copy

class Link(node.Node):
    def __init__(self, mode="basic", rect=pygame.Rect(0,0,16,16)):
        self.mode = mode
        self.rect = rect
        if self.mode == "directed":
            self.image = pygame.image.load("../res/com_link_directed.png")
        else:
            self.image = pygame.image.load("../res/com_link_basic.png")
            
        self.pointer = copy.copy(self.image)
        self.links = []
        self.active_link = 0
        self.next_link_callback = None
        
    def advance_link(self):
        if len(self.links) == 0:
            return
        self.active_link = (self.active_link + 1) % len(self.links)
        self.rotate_towards(self.links[self.active_link].rect.center)
        
    def clicked_on(self):
        self.advance_link()
        
    def rotate_towards(self, pos):
        angle = math.degrees(math.atan2(pos[1] - self.rect.center[1], pos[0] - self.rect.center[0]))
        self.pointer = copy.copy(self.image)
        pygame.draw.line(self.pointer, (255,0,0), self.pointer.get_rect().center, (16*math.cos(angle), 16*math.sin(angle)), depth=6)
        #pygame.draw.arc(self.pointer, (255,0,0), pygame.Rect(0,0,32,32), angle - 10, angle + 10, 1)
        
    def draw(self):
        game.screen.blit(self.pointer, self.rect, depth=7)
        
    def draw_path(self):
        for link in self.links:
            game.screen.draw_line(self.rect.center, link.rect.center, depth=6)
            
    def next_link(self, caller=None):
        if self.next_link_callback is not None:
            self.next_link_callback(caller)
        if len(self.links) == 0:
            return None
        else:
            return random.choice(self.links)
            #return self.links[self.active_link]
        
def distance(a, b):
    return math.sqrt(math.pow(a[0]-b[0],2) + math.pow(a[1]-b[1], 2))
        
class Vote(node.Node):
    def __init__(self, controller=None, val=1, rect=pygame.Rect(0,0,16,16)):
        self.controller = controller
        self.rect = rect
        self.x = self.rect.x*1.0
        self.y = self.rect.y*1.0
        self.startpos = (self.x,self.y)
        self.val = val
        self.velocity = 1
        if self.val == -1:
            self.image = pygame.image.load("../res/com_vote_neg.png")
        else:
            self.image = pygame.image.load("../res/com_vote_pos.png")
        self.target = None
        
    def act(self):
        self.follow()
        
    def follow(self):
        if self.target is not None:
            dist = distance(self.target.rect.center, self.rect.center)
            dist2 = distance(self.startpos, self.rect.center)
            theta = math.atan2(self.target.rect.center[1]-self.rect.center[1], 
                                self.target.rect.center[0]-self.rect.center[0])
            self.move_vec((theta, self.velocity * min(1,(min(dist2, dist)+5)/100.0)))
            if self.target.rect.center == self.rect.center:
                self.startpos = self.target.rect.center
                self.target = self.target.next_link(self)
            
    def move_vec(self,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        self.x+=dx
        self.y+=dy
        self.rect.center = (self.x,self.y)
            
    def draw(self):
        game.screen.blit(self.image, self.rect, depth=8)


class Comment(node.Node):
    def __init__(self, text, index, rect=pygame.Rect(0,0,100,100)):
        self.rect = rect.copy()
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = (self.rect.x, self.rect.center[1])
        self.link = Link(rect=tmp_rect.copy())
        
        self.link.next_link_callback = self.add_vote
        
        self.text = text
        self.index = index
        self.upvotes = 0
        self.downvotes = 0
        self.upvote_rect =     pygame.Rect(self.rect.x + self.rect.height*.5, self.rect.y, self.rect.height, self.rect.height)
        self.downvote_rect = pygame.Rect(self.rect.right - self.rect.height*1.5, self.rect.y, self.rect.height, self.rect.height)
        self.create_link_cycle()
        
    def add_vote(self, v):
        if v.val > 0:
            self.upvotes += 1
        if v.val < 0:
            self.downvotes -= 1
        
    def create_link_cycle(self):
        r = pygame.Rect(0,0,16,16)
        self.link_cycle = []
        r.center = self.rect.bottomleft
        a = Link(rect=r.copy())
        r.center = self.rect.bottomright
        b = Link(rect=r.copy())
        r.center = self.rect.topright
        c = Link(rect=r.copy())
        r.center = self.rect.topleft
        d = Link(rect=r.copy())
        self.link.links.append(a)
        a.links.append(b)
        b.links.append(c)
        c.links.append(d)
        d.links.append(a)
        
    def draw(self):
        game.screen.draw_outline(self.rect, width=1, depth=7)
        game.screen.draw_text(self.text, rect=self.rect, scaling=True, centered=True, depth=8)
        game.screen.draw_text('+' + str(self.upvotes), color=(170,255,170), rect=self.upvote_rect, scaling=True, centered=True, depth=8)
        game.screen.draw_text(str(self.downvotes), color=(255,170,170), rect=self.downvote_rect, scaling=True, centered=True, depth=8)


class CommentGame(node.Node):
    def __init__(self):
        super(CommentGame, self).__init__()
        self.links = []
        self.votes = []
        self.wave_val = 1
        self.wave_cooldown = self.wave_clock = 5000
        self.wave_range = (25,50)
        self.generate()
        
    def generate(self, com1="Comment 1", com2="Comment 2", com3="Comment 3"):
        self.com1 = Comment(com1, 1, rect=pygame.Rect(100,600,800,90))
        self.com2 = Comment(com2, 2, rect=pygame.Rect(100,700,800,90))
        self.com3 = Comment(com3, 3, rect=pygame.Rect(100,800,800,90))
        self.create_links_v1()
        self.create_votes()
    
    
    def create_links_v1(self):
        length = 8
        for i in range(length):
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (i*(800/length)+150, 0*50+400)
            tmp = Link(rect = tmp_rect.copy())
            self.links.append(tmp)
        
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (i*(800/length)+150, 1*50+400)
            tmp = Link(rect = tmp_rect.copy())
            self.links.append(tmp)
        
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (i*(800/length)+150, 2*50+400)
            tmp = Link(rect = tmp_rect.copy())
            self.links.append(tmp)
            
        for i in range(len(self.links)-3):
            self.links[i].links.append(self.links[i+1])
            self.links[i].links.append(self.links[i+2])
            self.links[i].links.append(self.links[i+3])
            
        for link in self.links:
            for i in range(random.randint(2,4)):
                link.advance_link()
            
        a = self.links[-3]
        b = self.links[-2]
        c = self.links[-1]
            
        self.join_links(a, self.com1.link, 32)
        self.join_links(b, self.com2.link, 24)
        self.join_links(c, self.com3.link, 16)
        
    def join_links(self, a, b, x):
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = a.rect.center
        tmp_rect.move_ip(x+b.rect.center[0]/2,0)
        topright = Link(rect = tmp_rect.copy())
        self.links.append(topright)
        a.links.append(topright)
        
        tmp_rect.move_ip(0, x*8-96)
        right = Link(rect=tmp_rect.copy())
        self.links.append(right)
        topright.links.append(right)
        
        tmp_rect.move_ip(-a.rect.center[0], 0)
        left = Link(rect=tmp_rect.copy())
        self.links.append(left)
        right.links.append(left)
        
        tmp_rect.center = (tmp_rect.center[0], b.rect.center[1])
        bottomleft = Link(rect=tmp_rect.copy())
        self.links.append(bottomleft)
        left.links.append(bottomleft)
        
        bottomleft.links.append(b)
        
    def create_links_random(self):
        length = 10
        for i in range(length):
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (random.randint(50,950), random.randint(50,950))
            tmp = Link(rect = tmp_rect.copy())
            self.links.append(tmp)
            
        for i in range(len(self.links)-1):
            self.links[i].links.append(self.links[i+1])
            self.links[i].links.append(self.links[random.randint(0,len(self.links)-1)])
            
        for link in self.links:
            link.advance_link()
            
        self.links[len(self.links)-1].links.append(self.links[0])
            
    def create_votes(self, amount=100, value=1):
        for i in range(amount):
            self.create_vote(value)
    
    def create_vote(self, value=1):
        tmp_rect = pygame.Rect(0,0,10,10)
        tmp = Vote(rect=tmp_rect,val=value)
        tmp.velocity = random.uniform(2.0,4.0)
        tmp.target = self.links[0]
        self.votes.append(tmp)
    
    def act(self):
        self.wave_spawner()
        for vote in self.votes:
            vote.act()
    
    def wave_spawner(self):
        self.wave_clock -= game.dt
        if self.wave_clock <= 0:
            self.wave_clock = self.wave_cooldown + random.randint(0,500)*.001
            self.wave_val *= -1
            self.create_votes(random.randint(self.wave_range[0], self.wave_range[1]), self.wave_val)
    
    def draw(self):
        self.com3.draw()
        self.com2.draw()
        self.com1.draw()
        for link in self.links:
            link.draw_path()
        for link in self.links:
            link.draw()
        for vote in self.votes:
            vote.draw()
            
    def input(self, events):
        for s in self.links:
            s.click_check(events)
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.paused:
                pass
        
        
if __name__ == '__main__':
    game.init()
    game.screen = screen.Screen()
    cg = CommentGame()
    cg.act()
    cg.draw()
        
