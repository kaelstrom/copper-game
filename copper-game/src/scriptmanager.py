import choicenode
import stringswapgame
import pygame
import stringnode
import emailnode
import node
import game
import script
from pprint import pprint

class ScriptManager(object):
    def __init__(self, script_file):
        self.scenes = {}
        self.day = 1
        self.active_node = None
        self.scripts = {}
        #self.dummy()
        self.parse_file(script_file)
        self.generate_nodes()
        
    def dummy(self):
        test = node.Node()
        
        self.scenes['0'] = emailnode.test_email()
        
        self.scenes['1'] = game.teen
        
        self.active_node = self.scenes['0']
        
    def parse_file(self, script_file):
        blocks = open(script_file, 'r').read().split('%%%')
        for b in blocks:
            if len(b.split('%%')) == 2:
                args = b.split('%%')[0].lower().split('\n')
                text = b.split('%%')[1]
                tmp = script.Script()
                tmp.text = text
                for pair in args:
                    if pair is not None:
                        pair = pair.split(' ')
                        if len(pair) == 2:
                            tmp.__dict__[pair[0]] = pair[1]
                            
                self.scripts[tmp.id] = tmp
          
        for key, val in self.scripts.items():
            pprint(vars(val))
            
    def generate_nodes(self):
        for key, val in self.scripts.items():
            if val.mode == 'email':
                self.scenes[key] = emailnode.from_script(val)