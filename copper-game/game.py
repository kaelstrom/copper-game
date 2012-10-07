'''  config variables and intermodule references  '''

import pygame

game = None
screen = None
font_arial = None
font_tempesta = None

def init():
    global font_arial, font_tempesta
    pygame.init()
    font_arial = pygame.font.SysFont("arial", 48)
    font_tempesta = pygame.font.Font("tempesta.ttf", 8)