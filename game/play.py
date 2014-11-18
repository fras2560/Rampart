'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 11/14/2014
@note: Used to create the game
'''
from rampart import Rampart
from rampart.controls import PLAYERONE, PLAYERTWO
import os
level = os.path.join(os.getcwd(), 'levels', 'LevelOne.txt')
game = Rampart(2, level)
game.set_player_controls(1, PLAYERONE)
game.set_player_controls(2, PLAYERTWO)
play = True
while play:
    play = game.game_tick()