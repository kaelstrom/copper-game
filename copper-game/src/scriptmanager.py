import choicenode
import contactnode
import stringswapgame
import pygame
import stringnode
import emailnode
import node
import game
import script
import uservaluenode
from pprint import pprint

class ScriptManager(object):
    def __init__(self, script_file, contact_file):
        game.scriptmanager = self
        self.scenes = {}
        self.day = 1
        self.active_node = None
        self.scripts = {}
        self.contacts = {}
        self.parse_contact_file(contact_file)
        self.parse_script_file(script_file)
        self.generate_nodes()
        game.contacts = self.contacts
        game.scenes = self.scenes
        self.next_scene()
        
    def load_scene(self, scene):
        val = self.scenes[scene]
        val.scene_viewed = True
        game.active_node = self.active_node = val
        
    def next_scene(self):
        sort = sorted(self.scenes, key=self.scenes.get)
        sort = sorted([int(x) for x in sort])
        for key in sort:
            val = self.scenes[str(key)]
            if val.scene_viewed == False:
                val.scene_viewed = True
                game.active_node = self.active_node = val
                return
        
    def parse_script_file(self, script_file):
        count = 0
        blocks = open(script_file, 'r').read().split('%%%')
        for b in blocks:
            if len(b.split('%%')) == 2:
                args = b.split('%%')[0].split('\n')
                text = b.split('%%')[1]
                tmp = script.Script()
                tmp.text = text
                for pair in args:
                    if pair is not None:
                        pair = pair.split(' ')
                        if len(pair) > 1:
                            tmp.__dict__[pair[0].lower()] = ' '.join(pair[1:])
                            
                            
                self.scripts[str(count) + tmp.id] = tmp
                count+=1
          
        #for key, val in self.scripts.items():
        #    pprint(vars(val))
            
    def parse_contact_file(self, contact_file):
        blocks = open(contact_file, 'r').read().split('%%%')
        for b in blocks:
            if len(b) != 0:
                args = b.split('\n')
                tmp = contactnode.ContactNode()
                for pair in args:
                    if pair is not None:
                        pair = pair.split(' ')
                        if len(pair) > 1:
                            tmp.__dict__[pair[0].lower()] = ' '.join(pair[1:])
                            
                tmp.load_image(tmp.image)
                self.contacts[tmp.name.lower()] = tmp
        
        #for key, val in self.contacts.items():
        #   pprint(vars(val))
        self.contacts['unknown'] = contactnode.ContactNode()
        game.teen = self.contacts['john']
        print game.teen
        game.teenvalue = uservaluenode.make_user(game.teen)
        print game.teenvalue
        game.contacts = self.contacts
            
    def generate_nodes(self):
        for key, val in self.scripts.items():
            if val.mode == 'email':
                print vars(val)
                self.scenes[key] = emailnode.from_script(val)