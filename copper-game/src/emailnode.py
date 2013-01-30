import node
import textnode
import pygame
import choicenode
import game
import uservaluenode
import continuenode
import contactnode
import scrollbox
import helpnode

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
        self.add(helpnode.HelpNode("This is the email viewer. From this screen you can intercept communication and manipulate words that are flashing. These changes will affect John's values displayed in the bottom right. When you are done with an email, hit continue to apply the changes and move on.")) 
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
        self.vals = [self.swap1vals, self.swap2vals]
        print self.vals
        tmp = scrollbox.ScrollBox()
        tmp.parent = self
        tmp.generate(self.text, self.vals, pygame.Rect(50,230,900,460))
        
        self.add(tmp)
        self.add(continuenode.ContinueNode(rect=pygame.Rect(600,800,240,60)))
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
    
    