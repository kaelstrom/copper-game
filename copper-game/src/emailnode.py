import node
import textnode
import pygame
import choicenode
import game
import uservaluenode
import continuenode
import contactnode

class EmailNode(node.Node):
    def __init__(self, text="", vals=None, rect=pygame.Rect(0,0,1000,1000)):
        super(EmailNode, self).__init__()
        self.teenvalue = None
        if game.teenvalue is not None:
            self.teenvalue = game.teenvalue
        elif game.teen is not None:
            self.teenvalue = (uservaluenode.make_user(game.teen))
            game.teenvalue = self.teenvalue
        self.vals = vals
        if self.vals is None:
            self.vals = [[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]
        self.from_contact = None
        self.to_contact = None
        self.sender = None
        self.to = None
        self.rect = rect
        self.text = text
        #self.generate(text, rect)
        
    def draw(self):
        
        from_rect = pygame.Rect(100,50,150,150)
        to_rect = pygame.Rect(750,50,150,150)
        color = (180,180,180)
        
        if self.from_contact is not None:
            game.screen.draw_outline(from_rect.inflate(10,10), color, 2)
            game.screen.blit(self.from_contact.image, from_rect)
            game.screen.draw_text('From: ' + self.from_contact.name, pygame.Rect(260, 60,700,64), scaling=True, plasma=False)
            game.screen.draw_outline(pygame.Rect(from_rect.inflate(10,10).right, 110, (to_rect.inflate(10,10).left-from_rect.inflate(10,10).right)-40, 1), color, 2)
        if self.to_contact is not None:
            game.screen.draw_outline(to_rect.inflate(10,10), color, 2)
            game.screen.blit(self.to_contact.image, to_rect)
            game.screen.draw_text('To: ' + self.to_contact.name, pygame.Rect(300, 120,700,64), scaling=True, plasma=False)
            game.screen.draw_outline(pygame.Rect(from_rect.inflate(10,10).right+40, 170, (to_rect.inflate(10,10).left-from_rect.inflate(10,10).right)-40, 1), color, 2)
            
    def generate(self, text, rect):
        if self.sender is None:
            self.sender = 'unknown'
        if self.sender.lower() not in game.contacts:
            print 'sender ' + self.sender + ' not found'
            self.sender = 'unknown'
            
        self.from_contact = game.contacts[self.sender.lower()]
            
        if self.to is None:
            self.to = 'unknown'
        if self.to.lower() not in game.contacts:
            print 'recipient ' + self.to + ' not found'
            self.to = 'unknown'
            
        self.to_contact = game.contacts[self.to.lower()]
            
        self.text = text
        self.rect = rect.move(50,180)
        self.rect.width = 900
        self.lines = self.text.split('\n')
        #spacing = 1.0/len(self.lines)
        spacing = 60
        self.disp_rect = self.rect.inflate(1, spacing/rect.height)
        self.disp_rect.height = 60
        self.children = []
        self.choicenodes = []
        c = 0
        for line in self.lines:
            if '{' not in line and '}' not in line:
                tmp = textnode.TextNode(line, self.disp_rect.copy())
                tmp.scaling=True
                self.add(tmp)
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
                self.add(tmp)
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
                
        self.choicenodes.reverse()
        for c in self.choicenodes:
            self.add(c)
        self.add(continuenode.ContinueNode())
        self.add(game.teenvalue)

def test_email():
        tmp = EmailNode(
            "  Commercial property has been\n" +
            "  doing well for a while, and it\n" +
            "  appears the {residential|automotive}market \n" +
            "  is now following.{Sellers|Buyers} have \n" +
            "  a big chance to profit soon.",
            [[[0,0,0],[3,0,0]],[[-2,0,0],[4,0,2]]],
            pygame.Rect(100,100,800,800))
        tmp.generate(tmp.text, tmp.rect)
        return tmp
            
def from_script(script):
    tmp = EmailNode()
    for pair in vars(script).items():
        tmp.__dict__[pair[0]] = pair[1]
    tmp.generate(tmp.text, tmp.rect)
    return tmp
    
    