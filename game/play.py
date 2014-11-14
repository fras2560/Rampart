'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 11/14/2014
@note: Used to create the game
'''
from rampart import Rampart
from rampart.config import BUILDINGBASE
import pygame
import os
level = os.path.join(os.getcwd(), 'levels', 'test-building-map.txt')
game = Rampart(2, level)
play = True
while play:
    play = game.game_tick()
pygame.quit()