import node
import game
import pygame
import screen
import random
import math
import copy
import continuenode
import helpnode

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
        self.degrade = 1
        self.interactive = False
        self.pulse = 0
        self.pulse_inc = 0
        self.pulse_rate = .01
        self.pulse_height = 4.0
        self.degrade_rate = .0003
        self.seed = random.uniform(0.0, 100.0)
        
    def advance_link(self):
        self.degrade = 1.5 + random.uniform(0.0, 0.5)
        if len(self.links) == 0:
            return
        self.active_link = (self.active_link + 1) % len(self.links)
        self.rotate_towards(self.links[self.active_link].rect.center)
      
    def input(self, events):
        for e in events:
                if e.type == pygame.MOUSEBUTTONUP:
                    if game.screen.scale_rect(self.rect.inflate(32,32)).collidepoint(pygame.mouse.get_pos()):
                        self.advance_link()
        
    #def clicked_on(self):
    #    self.advance_link()
        
    def rotate_towards(self, pos):
        angle = math.degrees(math.atan2(pos[1] - self.rect.center[1], pos[0] - self.rect.center[0]))
        self.pointer = copy.copy(self.image)
        #pygame.draw.line(self.pointer, (255,0,0), self.pointer.get_rect().center, (16*math.cos(angle), 16*math.sin(angle)), depth=6)
        #pygame.draw.arc(self.pointer, (255,0,0), pygame.Rect(0,0,32,32), angle - 10, angle + 10, 1)
        
    def draw(self):
        if self.interactive:
            game.screen.blit(self.pointer, self.rect.inflate(4+self.pulse, 4+self.pulse), depth=9)
        else:
            game.screen.blit(self.pointer, self.rect, depth=9)
        
    def act(self):
        self.pulse_inc += self.pulse_rate * game.dt
        self.pulse = self.pulse_height * math.sin(self.pulse_inc+self.seed)
        if self.interactive:
            self.degrade -= self.degrade_rate *random.uniform(0.0,1.0) * game.dt
            if self.degrade <= 0:
                self.advance_link()
        
    def draw_path(self):
        if self.interactive:
            for link in self.links:
                game.screen.draw_line(self.rect.center, link.rect.center, color=(0,0,20), depth=6)
            game.screen.draw_line(self.rect.center, self.links[self.active_link].rect.center, color=(0,0,min(255, 20+230*self.degrade)), depth=7)
        else:
            for link in self.links:
                game.screen.draw_line(self.rect.center, link.rect.center, color=(0,0,255), depth=6)
            
            
    def next_link(self, caller=None):
        if self.next_link_callback is not None:
            self.next_link_callback(caller)
        if len(self.links) == 0:
            return None
        else:
            if self.interactive:
                return self.links[self.active_link]
            else:
                return random.choice(self.links)
        
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
    def __init__(self, text, index=-1, rect=pygame.Rect(0,0,100,100),mode="comment"):
        self.rect = rect.copy()
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = (self.rect.right, self.rect.center[1])
        self.link = Link(rect=tmp_rect.copy())
        
        self.link.next_link_callback = self.add_vote
        
        self.mode = mode
        self.text = text
        self.index = index
        self.upvotes = 0
        self.downvotes = 0
        self.upvote_rect =     pygame.Rect(self.rect.x + self.rect.height*.5, self.rect.y, self.rect.height, self.rect.height)
        self.downvote_rect = pygame.Rect(self.rect.right - self.rect.height*1.5, self.rect.y, self.rect.height, self.rect.height)
        self.text_rect_a = pygame.Rect(self.upvote_rect.right, self.rect.y, self.downvote_rect.left - self.upvote_rect.right,self.rect.height/2)
        self.text_rect_b = self.text_rect_a.move(0,self.text_rect_a.height)
        index = self.text.find(' ', len(self.text)/2)
        self.text_a = self.text[:index]
        self.text_b = self.text[index:]
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
        self.link.links.append(c)
        a.links.append(b)
        b.links.append(c)
        c.links.append(d)
        d.links.append(a)
        
    def draw(self):
        game.screen.draw_outline(self.rect, width=1, depth=7)
        game.screen.draw_text(self.text_a, rect=self.text_rect_a, scaling=True, centered=True, depth=8)
        game.screen.draw_text(self.text_b, rect=self.text_rect_b, scaling=True, centered=True, depth=8)
        if self.mode == "comment":
            game.screen.draw_text('+' + str(self.upvotes), color=(170,255,170), rect=self.upvote_rect, scaling=True, centered=True, depth=8)
            game.screen.draw_text(str(self.downvotes), color=(255,170,170), rect=self.downvote_rect, scaling=True, centered=True, depth=8)


class CommentGame(node.Node):
    def __init__(self, mode="game"):
        super(CommentGame, self).__init__()
        self.scene_viewed = False
        self.scene_skipped = False
        self.condition = True
        self.links = []
        self.votes = []
        self.wave_val = 1
        self.waves = 10
        self.waves_active = False
        self.wave_cooldown = self.wave_clock = 7000
        self.wave_range = (25,50)
        self.mode = mode
        if self.mode == "game":
            self.generate()
            self.add(helpnode.HelpNode("This is the research viewer. A headline is shown at the top and responding comments are at the bottom. Redirect upvotes and downvotes by clicking the pulsing nodes in the switchboard. Nodes will automatically change over time. Once all votes go through, the winning comment will determine John's outlook." )) 
        
        elif self.mode == "title":
            self.create_title()
            
    def create_title(self):
        disp_height = 950
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = (0,disp_height)
        tmp = Link(rect = tmp_rect.copy())
        self.links.append(tmp)
        
        tmp_rect.center = (1000,disp_height)
        tmp = Link(rect = tmp_rect.copy())
        self.links.append(tmp)
        
        tmp_rect.center = (1050,disp_height)
        tmp = Link(rect = tmp_rect.copy())
        self.links.append(tmp)
        
        tmp_rect.center = (1050,1050)
        tmp = Link(rect = tmp_rect.copy())
        self.links.append(tmp)
        
        tmp_rect.center = (-50,1050)
        tmp = Link(rect = tmp_rect.copy())
        self.links.append(tmp)
        
        tmp_rect.center = (-50,disp_height)
        tmp = Link(rect = tmp_rect.copy())
        self.links.append(tmp)
        
        for i in range(len(self.links)-1):
            self.links[i].links.append(self.links[i+1])
            
        self.links[-1].links.append(self.links[0])
        
        for i in range(40):
            self.create_vote()
            self.votes[-1].y = 800
            self.votes[-1].x = random.uniform(-4000,-100)
        
        
    def generate(self, art="Article", com1="Comment 1", com1r=(0,0,0,"art1 - com1 chosen"),
                                                        com2="Comment 2", com2r=(0,0,0,"art1 - com2 chosen"),
                                                        com3="Comment 3", com3r=(0,0,0,"art1 - com3 chosen")):
        self.links = []
        self.votes = []
        self.waves_rect = pygame.Rect(10, 10, 100,100)
        self.begin_button = continuenode.ContinueNode("BEGIN", 
                                                                                rect=pygame.Rect(100, 10, 200, 80),
                                                                                callback=self.begin_waves)
        self.article =Comment(art,         rect=pygame.Rect(100,100,800,90),mode='article')
        self.com1 = Comment(com1, 1, rect=pygame.Rect(100,600,800,90))
        self.com2 = Comment(com2, 2, rect=pygame.Rect(100,700,800,90))
        self.com3 = Comment(com3, 3, rect=pygame.Rect(100,800,800,90))
        self.header_article =         pygame.Rect(410,60,180,40)
        self.header_switchboard = pygame.Rect(410,235,180,40)
        self.header_comment =     pygame.Rect(410,560,180,40)
        self.switch_bg_rect = pygame.Rect(75,275, 850, 250)
        self.create_links_v1()
        #self.create_votes()
    
    def slink(self, child, index):
        if index >= 0 and index < len(self.links):
            self.links[index].links.append(child)
    
    def create_links_v1(self):
        length = 2
        for i in range(length+1):
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (i*(800/length)+100+32*0, 0*100+300)
            tmp = Link(rect = tmp_rect.copy())
            self.slink(tmp, i*3-1)
            self.slink(tmp, i*3-2)
            self.slink(tmp, i*3-3)
            self.links.append(tmp)
            
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (i*(800/length)+100+32*0, 1*100+300)
            tmp = Link(rect = tmp_rect.copy())
            self.slink(tmp, i*3-1)
            self.slink(tmp, i*3-2)
            self.slink(tmp, i*3-3)
            self.links.append(tmp)
        
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (i*(800/length)+100+32*0, 2*100+300)
            tmp = Link(rect = tmp_rect.copy())
            self.slink(tmp, i*3-1)
            self.slink(tmp, i*3-2)
            self.slink(tmp, i*3-3)
            self.links.append(tmp)
            
        #for i in range(len(self.links)-3):
        #    for j in (3,4,5):
        #        if i + j < len(self.links):
        #            self.links[i].links.append(self.links[i+j])
            
        for i in range(len(self.links)-3):
            self.links[i].interactive = True
            
        for link in self.links:
            for i in range(random.randint(2,4)):
                link.advance_link()
            
        a = self.links[-3]
        b = self.links[-2]
        c = self.links[-1]
            
        self.join_links(c, self.com1.link, 16)
        self.join_links(b, self.com2.link, 24)
        self.join_links(a, self.com3.link, 32)
        
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = (50, 400)
        tmp = Link(rect = tmp_rect.copy())
        tmp.interactive = False
        tmp.links.append(self.links[0])
        tmp.links.append(self.links[1])
        tmp.links.append(self.links[2])
        self.links.append(tmp)
        
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = (24, 400)
        tmp = Link(rect = tmp_rect.copy())
        tmp.interactive = False
        tmp.links.append(self.links[-1])
        self.links.append(tmp)
        
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = (24, -10)
        tmp = Link(rect = tmp_rect.copy())
        tmp.interactive = False
        tmp.links.append(self.links[-1])
        self.links.append(tmp)
        
    def join_links(self, a, b, x):
        tmp_rect = pygame.Rect(0,0,16,16)
        tmp_rect.center = a.rect.center
        tmp_rect.move_ip(x*2+a.rect.width/2,0)
        topright = Link(rect = tmp_rect.copy())
        self.links.append(topright)
        a.links.append(topright)
        
        tmp_rect.center = (tmp_rect.center[0], b.rect.center[1])
        bottomright = Link(rect=tmp_rect.copy())
        self.links.append(bottomright)
        topright.links.append(bottomright)
        
        bottomright.links.append(b)
        
        #tmp_rect.move_ip(0, x*8-96)
        #right = Link(rect=tmp_rect.copy())
        #self.links.append(right)
        #topright.links.append(right)
        
        #tmp_rect.move_ip(-a.rect.center[0], 0)
        #left = Link(rect=tmp_rect.copy())
        #self.links.append(left)
        #right.links.append(left)
        
        #tmp_rect.center = (tmp_rect.center[0], b.rect.center[1])
        #bottomleft = Link(rect=tmp_rect.copy())
        #self.links.append(bottomleft)
        #left.links.append(bottomleft)
        
        #bottomleft.links.append(b)
        
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
            
    def create_votes(self, amount=50, value=1):
        for i in range(amount):
            self.create_vote(value)
    
    def create_vote(self, value=1):
        tmp_rect = pygame.Rect(self.links[-1].rect.x,self.links[-1].rect.y,10,10)
        tmp = Vote(rect=tmp_rect,val=value)
        tmp.velocity = random.uniform(2.0,2.5)
        tmp.target = self.links[-1]
        self.votes.append(tmp)
    
    def act(self):
        if self.mode == 'game':
            self.wave_spawner()
            self.begin_button.act()
        for vote in self.votes:
            vote.act()
            
        for link in self.links:
            link.act()
    
    def begin_waves(self):
        self.waves_active = True
        self.wave_clock = 0
    
    def wave_spawner(self):
        if self.waves == 0:
            self.waves_active = False
        if self.waves_active:
            self.wave_clock -= game.dt
            if self.wave_clock <= 0:
                self.waves -= 1
                self.wave_clock = self.wave_cooldown + random.randint(0,500)*.001
                self.wave_val *= -1
                self.create_votes(random.randint(self.wave_range[0], self.wave_range[1]), self.wave_val)
    
    def draw(self):
        if self.mode == 'game':
            self.com3.draw()
            self.com2.draw()
            self.com1.draw()
            self.article.draw()
            self.begin_button.draw()
            #game.screen.draw_outline(self.waves_rect, depth=3)
            game.screen.draw_text(str(self.waves), color=(255,255,255), rect=self.waves_rect, scaling=True, centered=True, depth=8)
            game.screen.draw_text('waves', color=(255,255,255), 
                                                rect=pygame.Rect(self.waves_rect.x, self.waves_rect.y, self.waves_rect.width, self.waves_rect.height/4), 
                                                scaling=True, centered=True, depth=8)
            game.screen.draw_outline(self.switch_bg_rect, depth=3)
            game.screen.draw_outline(self.header_article, width=1, depth = 4)
            game.screen.draw_outline(self.header_switchboard, width=1, depth = 4)
            game.screen.draw_outline(self.header_comment, width=1, depth = 4)
            game.screen.draw_text("Headline", rect=self.header_article, scaling=True, centered=True, depth=5)
            game.screen.draw_text("Switchboard", rect=self.header_switchboard, scaling=True, centered=True, depth=5)
            game.screen.draw_text("Comments", rect=self.header_comment, scaling=True, centered=True, depth=5)
        
        for link in self.links:
            link.draw_path()
        for link in self.links:
            link.draw()
        for vote in self.votes:
            vote.draw()
            
    def input(self, events):
        if self.mode != 'title':
            self.begin_button.input(events)
            for s in self.links:
                s.input(events)
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.paused:
                pass
        
        
def from_script(val):
    result = CommentGame()
    result.generate(val.article, val.comment1, val.comment1result,
                                            val.comment2, val.comment2result,
                                            val.comment3, val.comment3result)
    return result
    
if __name__ == '__main__':
    game.init()
    game.screen = screen.Screen()
    cg = CommentGame()
    cg.act()
    cg.draw()
        
