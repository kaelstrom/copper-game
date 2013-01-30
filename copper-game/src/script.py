class Script(object):
    def __init__(self):
        self.day=0
        self.spending=(0,0)
        self.political=(0,0)
        self.suspicion=(0,0)
        self.sender= 'unknown'
        self.to = 'unknown'
        self.id = ''
        self.mode = 'email'
        self.condition = True
        self.scene_skipped = False
        self.swap1vals =[[0,0,0],[0,0,0]]
        self.swap2vals = [[0,0,0],[0,0,0]]
        self.swap1blurbs = None
        self.swap2blurbs = None
        