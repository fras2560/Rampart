'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 04/05/2014
@note: This class is used to store a collection of cannons
'''
from castle import Castle
import pygame
class Castles(pygame.sprite.Sprite):
    '''
    a class to hold all the castles and way to interact with all the cannons
    '''
    def __init__(self):
        '''
        towers: a list of towers
        '''
        self.towers = []

    def __len__(self):
        '''
        a function to find the numbers of castles in the set
        Parameters:
            None
        Returns:
            int: the number of castles
        '''
        return len(self.towers)

    def add(self,point):
        '''
        a function to add a castle to the set
        Parameters:
            point: The point of the top left of the castle
        Returns:
            None
        '''
        tower = Castle()
        tower.set(point)
        self.towers.append(tower)

    def delete(self):
        '''
        a function to delete all the towers
        Parameters:
            None
        Returns:
            None
        '''
        while len(self.towers) != 0:
            self.towers.pop()

    def draw(self,surface):
        '''
        a function to draw all the towers
        Parameters:
            surface: the surface to draw upon
        Returns:
            None
        '''
        for tower in self.towers:
            tower.draw(surface)

    def get(self):
        '''
        a function that gets all the castles positions
        Parmaeters:
            None
        Returns:
            list of points
        '''
        points = []
        for tower in self.towers:
            points.append(tower.get())
        return points

