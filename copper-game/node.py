'''
Created on Sep 30, 2012

@author: kaelstrom
'''

class Node(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.children = []
    
    
    def draw_all(self):
        self.draw()
        for child in self.children:
            child.draw_all()
            
    def draw(self):
        pass