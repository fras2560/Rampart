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
from player import Player
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
        self.player_one = Player()
        self.player_two = Player()

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
        self.player_one.draw(surface)
        self.player_two.draw(surface)

    def save(self):
        '''
        a function to save a game
        Parameters:
            None
        Returns:
            None
        '''
        self.game.save_level()

    def load(self, file):
        '''
        a function to load the game
        Parameters:
            file: the file to load
        Returns:
            None
        '''
        self.game.load_level()

    def add(self,type,pos, player=None):
        '''
        a function to add type of object to the rampart game
        Parameters:
            type: the type of object to add
            pos: the position to add the obejct to
            player: if needed specify which player the object belongs to
        Returns:
            None
        '''
        (x,y) = pos.get()
        if type == GRASS:
            self.game.update_square(x,y,type)
        elif type == CANNON:
            self.game.update_square(x,y,type)
            if player is not None and player == 1:
                self.player_one.add(type,pos)
            elif player is not None and player == 2:
                self.player_two.add(type,pos)
        elif type == CASTLE:
            self.game.update_square(x,y,type)
            self.game.update_square(x+TERRAIN,y,type)
            self.game.update_square(x,y+TERRAIN,type)
            self.game.update_square(x+TERRAIN,y+TERRAIN,type)
            
            if player is not None and player == 1:
                self.player_one.add(type,pos)
            elif player is not None and player == 2:
                self.player_two.add(type,pos)