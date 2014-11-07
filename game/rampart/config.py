'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 30/04/2014
@note: A place to hold various constants and game configurations
'''
from math import pi
import os
SIZE = (500, 500)
'''
directions"
'''
DOWN = 1
UP = -1
LEFT = -1
RIGHT = 1
'''
a list of game modes
'''
BUILDING = 0
SHOOTING = 1
'''
list of assets Images
'''
I_CANNON = 'cannon.png'
O_GRASS_NORMAL = 'grass-odd.png'
E_GRASS_NORMAL = 'grass-even.png'
I_GRASS_DESTROYED = 'grass.png'
I_GRASS_PAINTED = "grass.png"
O_WATER = 'sea-odd.png'
E_WATER = 'sea-even.png'

I_WALL = 'wall.png'
I_CASTLE = 'castle.png'
I_CASTLE_1 = 'castle_1.png'
I_CASTLE_2 = 'castle_2.png'
I_CASTLE_3 = 'castle_3.png'
I_BLOCK = 'wall.png'
BASE = os.path.join(os.path.dirname(os.getcwd()),'levels', 'base.txt')
'''
Node Types and Constants
'''
EMPTY = 0
BLOCK = 1
CANNON = 2
GRASS = 3
WATER = 4
WALL = 5
CASTLE = 6
PAINTED = 1
TERRAIN = 10 #terrain size
TYPES = [BLOCK, CANNON, GRASS, WATER, WALL, CASTLE]
TERRAIN_TO_FILE = {CANNON: [[I_CANNON]],
                   BLOCK: [[I_BLOCK]],
                   GRASS: [
                           [E_GRASS_NORMAL, O_GRASS_NORMAL], 
                           [I_GRASS_DESTROYED], [I_GRASS_PAINTED]
                          ],
                   WATER: [[E_WATER, O_WATER]],
                   CASTLE: [[I_CASTLE]],
                   WALL: [[I_WALL]]
                  }

CANBUILD = [GRASS]
NODE_SIZE = 10

'''
PICTURE INDEXES
'''
NORMAL = 0
DESTROYED = 1
PAINTED = 2
'''
Player constants
'''
NONPLAYER = 0
PLAYERONE = 1
PLAYERTWO = 2

'''
movements
'''
NO_MOVE = 0
CLOCKWISE = -pi/2
COUNTER_CLOCKWISE = pi/2
'''
Physics constants
'''
GRAVITY = -0.049
'''
Player constants
'''
LIVES = 3