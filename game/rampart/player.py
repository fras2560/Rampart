'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import helper
import pygame
from config import CASTLE, CANNON, LIVES

class Player():
    def __init__(self):
        '''
        this class is used for player interactions
        guns: a list to hold all the players cannons (Node)
        towers: a list to hold all the towers: (Node)
        points: the number of points the player has (int)
        lives: the number of lives the player has
        '''
        self.guns = []
        self.towers = []
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
        self.guns = []
        self.towers = []
        self.points = 0
        self.lives = LIVES

    def add_castle(self, castle):
        '''
        a method to add an castle to the player
        Parameters:
            castle: the castle node object (Node)
        Returns:
            None
        '''
        self.towers.append(castle)

    def add_cannon(self, cannon):
        '''
        a method to add a cannon to the player's arsenal
        Parameters:
            cannon: the cannon node object (Node)
        Returns:
            None
        '''
        self.guns.append(cannon)