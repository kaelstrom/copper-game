'''
Created on Sep 30, 2012

@author: kaelstrom
'''
import node

class TextNode(node.Node):
    '''
    classdocs
    '''


    def __init__(self, text=""):
        '''
        Constructor
        '''
        super(TextNode, self).__init__()
        self.text = text
        
    def draw(self):
        game.game.screen.draw_text(self.text)
        
        
import game