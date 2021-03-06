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
Defaults
'''
BACKGROUND = ( 255, 255, 255) # white

'''
Directions and Movements
'''
DOWN = 1
UP = -1
LEFT = -1
RIGHT = 1
SHOOT = 0
MOVE_UP = 1
MOVE_RIGHT = 2
MOVE_DOWN = 3
MOVE_LEFT = 4
LAY_PIECE = 5
ROTATE_RIGHT = 6
ROTATE_LEFT = 7
NO_MOVE = 0
CLOCKWISE = -pi/2
COUNTER_CLOCKWISE = pi/2

'''
Game Modes and Constants
'''
SPEED = 10
BUILDTIME = 300
SHOOTTIME = 200
PLACETIME = 200
BUILDING = 0
SHOOTING = 1
PLACING = 2
CLEANUP = 3
NOMODE = 2
GRAVITY = -0.049
LIVES = 3
NONPLAYER = 0
PLAYERONE = 1
PLAYERTWO = 2
ARC = 30
PLAYERCOLORS = [
                ( 255,   0,   0),
                (  13,   0, 252),
                ( 252, 130,   0),
               ]
'''
Explosion Images
'''
EXPLOSIONS = ['explosion_1.png',
              'explosion_2.png',
              'explosion_3.png',
              'explosion_4.png',
              'explosion_5.png',
              'explosion_6.png'
              ]
'''
Node Images
'''
I_CANNON = 'cannon.png'
O_GRASS_NORMAL = 'grass-odd.png'
E_GRASS_NORMAL = 'grass-even.png'
I_GRASS_DESTROYED = 'grass.png'
E_GRASS_UNPAINTED = "territory-even.png"
O_GRASS_UNPAINTED = "territory-odd.png"
O_WATER = 'sea-odd.png'
E_WATER = 'sea-even.png'
O_EXTERIOR = "exterior-odd.png"
E_EXTERIOR = "exterior-even.png"
I_WALL = 'wall.png'
I_CASTLE = 'castle1.png'
I_CASTLE_1 = 'castle_1.png'
I_CASTLE_2 = 'castle_2.png'
I_CASTLE_3 = 'castle_3.png'
I_BLOCK = 'wall.png'
BASE = os.path.join(os.path.dirname(os.getcwd()),'levels', 'base.txt')
BUILDINGBASE = os.path.join(os.path.dirname(os.getcwd()),'levels',
                            'test-building-map.txt')
CASTLE_SPOTS= [(0, 0), (0, 1), (1, 0), (1,1), (0, 2), (1, 2)]

'''
Game Sounds
'''
EXPLOSION_SOUNDS = ['Explosion.wav','Explosion2.wav',
                     'Explosion3.wav', 'Explosion4.wav'
                ]
CANNON_SOUNDS = ['Cannon.wav', 'Cannon2.wav', 'Cannon3.wav']
APPLAUSE = 'Applause.wav'
END_TURN = 'EndTurn.wav'
WELCOME = 'Welcome.wav'
'''
Node Types, Constants, and Indexes
'''
EMPTY = 0
BLOCK = 1
CANNON = 2
GRASS = 3
WATER = 4
WALL = 5
CASTLE = 6
EXTERIOR = 7
PAINTED = 1
NODE_SIZE = 10
NORMAL = 0
DESTROYED = 1
UNPAINTED = 2
CANBUILD = [GRASS]
TYPES = [BLOCK, CANNON, GRASS, WATER, WALL, CASTLE, EXTERIOR]
# dict holds terrain and list of images
TERRAIN_TO_FILE = {CANNON: [
                            [I_CANNON],
                            [I_CANNON],
                            [I_CANNON]
                            ],
                   BLOCK: [
                           [I_BLOCK],
                           [I_GRASS_DESTROYED],
                           [I_BLOCK]
                           ],
                   GRASS: [
                           [E_GRASS_NORMAL, O_GRASS_NORMAL], 
                           [I_GRASS_DESTROYED],
                           [E_GRASS_UNPAINTED, O_GRASS_UNPAINTED]
                          ],
                   WATER: [
                           [E_WATER, O_WATER],
                           [E_WATER, O_WATER],
                           [E_WATER, O_WATER]
                          ],
                   CASTLE: [
                           [E_GRASS_NORMAL, O_GRASS_NORMAL], 
                           [I_GRASS_DESTROYED],
                           [E_GRASS_UNPAINTED, O_GRASS_UNPAINTED]
                           ],
                   WALL: [
                          [I_WALL],
                          [I_WALL],
                          [I_WALL]
                         ],
                   EXTERIOR: [
                              [E_EXTERIOR, O_EXTERIOR],
                              [E_EXTERIOR, O_EXTERIOR],
                              [E_EXTERIOR, O_EXTERIOR]
                             ]
                  }
CANBUILD = [GRASS]