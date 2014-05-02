'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 02/05/2014
@note: This class is used for rampart
'''

from terrain import Terrain
from matrix import Matrix
import os
import pygame
import unittest
from piece import Piece
from math import pi
from config import DOWN,UP,LEFT,RIGHT,EMPTY,BLOCK,CANNON,GRASS,PAINTED, WALL
from config import WATER,UP,DOWN,LEFT,RIGHT,NO_MOVE,CLOCKWISE,COUNTER_CLOCKWISE
from config import TERRAIN

class Rampart():
    def __init__(self):
        
        self.game = Matrix(row=50,column=50)
        self.grass = Terrain("grass.png")
        self.water = Terrain("sea.png")
        self.wall = Terrain("wall.png")
        
    def draw(self,surface):
        '''
        a function that draw the game board (grass, water, etc..)
        Parameters:
            surface: the screen on which to draw
        Returns:
            None
        '''
        y_pos = -TERRAIN
        for row in self.game._matrix:
            y_pos += TERRAIN
            x_pos = -TERRAIN
            for cell in row:
                x_pos += TERRAIN
                if cell == WALL:
                    self.wall.update(x=x_pos,y=y_pos)
                    self.wall.draw(surface)
                elif cell == WATER:
                    self.water.update(x=x_pos,y=y_pos)
                    self.water.draw(surface)
                elif cell == GRASS:
                    self.grass.update(x=x_pos,y=y_pos)
                    self.grass.draw(surface)