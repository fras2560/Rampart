'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
from cannon import Cannon
import pygame

class Cannons(pygame.sprite.Sprite):
    '''
    a class to hold all cannons and way to interact will the cannons
    '''
    def __init__(self):
        '''
        guns: a list of cannon
        '''
        self.guns = []

    def __len__(self):
        '''
        a function to find the numbers of cannons in the set
        Parameters:
            None
        Returns:
            int: the number of cannons
        '''
        return len(self.guns)

    def add(self, point):
        '''
        a function to add a cannon to the point given
        Parameters:
            point: the point of the cannon to add
        Returns:
            None
        '''
        gun = Cannon()
        gun.set(point)
        self.guns.append(gun)

    def delete(self):
        '''
        a function to delete all cannons
        Parameters:
            None
        Return
            None
        '''
        while len(self.guns) != 0:
            self.guns.pop()

    def draw(self, surface):
        '''
        a function to draw all the cannons
        Parameters:
            surface: the screen to draw on
        Returns:
            None
        '''
        for gun in self.guns:
            gun.draw(surface)

    def update(self):
        '''
        a function to update all the cannons and their firing sequence
        Parameters:
            None
        Returns:
            None
        '''
        for gun in self.guns:
            gun.update()

    def shoot(self, end):
        '''
        a function to shoot one available cannon
        Parameters:
            end: the point the cannon is aiming at
        Returns:
            None
        '''
        done = False
        pos = 0
        while not done and pos < len(self.guns):
            done = self.guns[pos].shoot(end)
            pos += 1

    def conflict(self,pos):
        '''
        a function to check if the position conflicts with any cannons
        Parameters:
            pos: the point to check if overlapp
        Returns:
            True if pos conflicts with a cannon
            False otherwise
        
        '''
        conflicting = False
        for gun in self.guns:
            if self.gun.conflict(pos):
                conflicting  = True
        return conflicting