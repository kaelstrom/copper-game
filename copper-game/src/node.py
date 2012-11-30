class Node(object):
    def __init__(self):
        self.children = []
        self.parent = None
        self.plasma = False
        self.scaling = False
        self.scene_viewed = False
    
    def add(self, n):
        n.parent = self
        self.children.append(n)
    
    def draw_all(self):
        self.draw()
        for child in self.children:
            child.draw_all()
            
    def set_all(self, var, val):
        self.__dict__[var] = val
        for child in self.children:
            child.set_all(var, val)
            
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