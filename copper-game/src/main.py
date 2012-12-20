import screen
import node
import stringnode
import textnode
import stringswapgame
import choicenode
import contactnode
import emailnode
import pygame
import game
import fx
import cProfile
import copy
import scriptmanager
import sound

class Game(object):
    def __init__(self):
        self.running = False
        game.init()
        self.screen = screen.Screen()
        game.game = self
        game.screen = self.screen
        self.clock = pygame.time.Clock()
        self.scene_num = 0
        self.scenes = []
        fx.init()
        
        self.ldraw = None
        self.activescenestack = []
        self.teen = contactnode.make_teen()
        game.teen = self.teen
        
        self.script = game.script = scriptmanager.ScriptManager("../res/script.txt", "../res/contacts.txt")
        #game.active_node = emailnode.test_email()
        sound.play_music()
    
    def start(self):
        self.main_loop()
        
    def main_loop(self):
        self.running = True
        while(self.running):
            game.dt = self.clock.tick(60)
            game.time += game.dt
            self.active_node = game.active_node
            self.input()
            self.act()
            self.draw()
        
    def input(self):
        events = pygame.event.get() 
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.scene_num = (self.scene_num + 1) % len(self.scenes)
                    self.active_node = self.scenes[self.scene_num]
                if event.key == pygame.K_RIGHT:
                    self.fade_to_scene(emailnode.test_email())
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        self.active_node.input_all(events)
                    
    def act(self):
        self.active_node.act_all()
        fx.update()
    
    def draw(self):
        self.screen.clear()
        self.active_node.draw_all()
        if self.ldraw is not None:
            self.ldraw()
            self.ldraw = None
        pygame.display.flip()
        
    def fade_to_scene(self, scene):
        game.active_node = scene
        
    def last_draw(self, func):
        self.ldraw = func
        
        
def initialize():
    g = Game()
    g.start()
    #cProfile.run('g.start()')
    
if __name__ == '__main__':
    initialize()