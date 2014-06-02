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

    def conflict(self,pos):
        '''
        a function to check if the position given is a conflicting with a castle
        Parameters:
            pos: the position to check (point)
        Returns:
            True if there is conflict
            False otherwise
        '''
        conflicting = False
        for tower in self.towers:
            if self.tower.conflict(pos):
                conflicting = True
                break;
        return conflicting

    def delete_castle(self,pos):
        '''
        a function to delete castle if conflicts with position given
        Parameters:
            pos: the position of comparison
        Returns:
            True if a castle was deleted
            False otherwise
        '''
        deleted = False
        castle = 0
        while not deleted and castle < len(self.towers):
            if self.towers[castle].conflict(pos):
                self.towers.pop(castle)
                deleted = True
            castle += 1
        return deleted