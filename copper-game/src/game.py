'''  config variables and intermodule references  '''

import pygame

game = None
screen = None
scriptmanager = None
active_node = None
contacts = {}
dt = 0
time = 0
font_arial = None
font_tempesta = None
teen = None
teenvalue = None

def init():
    global font_arial, font_tempesta
    pygame.init()
    font_arial = font_tempesta = pygame.font.Font("../res/tempesta.ttf", 8)