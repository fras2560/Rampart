'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import helper
import pygame
from cannons import Cannons
from castles import Castles
from config import CASTLE, CANNON, LIVES

class Player():
    def __init__(self):
        '''
        this class is used for player interactions
        guns: a list to hold all the players cannons
        towers: a list to hold all the towers:
        '''
        self.guns = Cannons()
        self.towers = Castles()
        self.points = 0
        self.lives = LIVES

    def reset(self):
        '''
        a that resets the player
        Parameters:
            None
        Returns:
            None
        '''
        self.guns.delete()
        self.towers.delete()
        self.points = 0
        self.lives = LIVES

    def draw(self,surface):
        '''
        a function to draw player's objects
        Parameters:
            surface: the surface to draw upon
        Returns:
            None
        '''
        self.guns.draw(surface)
        self.towers.draw(surface)
    
    def add(self, type, pos):
        '''
        a function to add an object to the player
        Parameters:
            type: the type of object to add
            pos: the position of the object to add
        Returns:
            None
        '''
        (x,y) = pos.get()
        if type == CANNON:
            self.guns.add(pos)
        elif type == CASTLE:
            #assume given top left point for castle
            self.towers.add(pos)