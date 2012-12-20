import node
import game
import pygame
import screen
import random
import math

class Link(node.Node):
    def __init__(self, mode="basic", rect=pygame.Rect(0,0,32,32)):
        self.mode = mode
        self.rect = rect
        if self.mode == "directed":
            self.image = pygame.image.load("../res/com_link_directed.png")
        else:
            self.image = pygame.image.load("../res/com_link_basic.png")
            
        self.links = []
        
    def draw(self):
        game.screen.blit(self.image, self.rect)
        
    def draw_path(self):
        for link in self.links:
            game.screen.draw_line(self.rect.center, link.rect.center)
            
    def next_link(self):
        if len(self.links) == 0:
            return None
        else:
            return self.links[0]
        
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
                self.target = self.target.next_link()
            
    def move_vec(self,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        self.x+=dx
        self.y+=dy
        self.rect.center = (self.x,self.y)
            
    def draw(self):
        game.screen.blit(self.image, self.rect)


class Comment(node.Node):
    def __init__(self, text, index):
        self.text = text
        self.index = index
        self.votes = 0


class CommentGame(node.Node):
    def __init__(self):
        super(CommentGame, self).__init__()
        self.links = []
        self.votes = []
        self.generate()
        
    def generate(self, com1="Comment 1", com2="Comment 2", com3="Comment 3"):
        self.com1 = Comment(com1, 1)
        self.com2 = Comment(com2, 2)
        self.com3 = Comment(com3, 3)
        self.create_links()
        self.create_votes()
    
    def create_links(self):
        length = 10
        for i in range(length):
            tmp_rect = pygame.Rect(0,0,16,16)
            tmp_rect.center = (((i*1.0)/length)*1000+50, random.randint(0,1000))
            tmp = Link(rect = tmp_rect.copy())
            self.links.append(tmp)
            
        for i in range(len(self.links)-1):
            self.links[i].links.append(self.links[i+1])
            
        self.links[len(self.links)-1].links.append(self.links[0])
            
    def create_votes(self):
        length = 100
        for i in range(length):
            tmp_rect = pygame.Rect(0,0,10,10)
            tmp = Vote(rect=tmp_rect)
            tmp.velocity = random.uniform(1.0,5.0)
            tmp.target = self.links[0]
            self.votes.append(tmp)
    
    def act(self):
        for vote in self.votes:
            vote.act()
    
    def draw(self):
        for link in self.links:
            link.draw_path()
        for link in self.links:
            link.draw()
        for vote in self.votes:
            vote.draw()
        self.com3.draw()
        self.com2.draw()
        self.com1.draw()
            
    def input(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.paused:
                pass
        
        
if __name__ == '__main__':
    game.init()
    game.screen = screen.Screen()
    cg = CommentGame()
    cg.act()
    cg.draw()
        
