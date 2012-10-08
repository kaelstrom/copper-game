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
    
    def add(self, n):
        self.children.append(n)
    
    def draw_all(self):
        self.draw()
        for child in self.children:
            child.draw_all()
            
    def draw(self):
        pass
    
    def act_all(self):
        self.act()
        for child in self.children:
            child.act_all()
            
    def act(self):
        pass
    
    def input_all(self, events):
        self.input(events)
        for child in self.children:
            child.input_all(events)
            
    def input(self, events):
        pass