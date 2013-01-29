import pygame
import game
import os

_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()
    
def play_music(filename = "../music/Secheron Peak - The Drift.mp3"):
    #secheron peak creative commons credit
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(-1, 0)