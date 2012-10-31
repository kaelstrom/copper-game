'''  config variables and intermodule references  '''

import pygame

game = None
screen = None
dt = 0
font_arial = None
font_tempesta = None
teen = None
teenvalue = None

def init():
    global font_arial, font_tempesta
    pygame.init()
    font_arial = pygame.font.SysFont("arial", 40)
    font_tempesta = pygame.font.Font("tempesta.ttf", 8)