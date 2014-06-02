'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used as the castle for rampart game
'''
import pygame
import helper
from config import TERRAIN
from color import Color

class Castle(pygame.sprite.Sprite):
    def __init__(self):
        self.active = False
        self.color = Color()
        fp = helper.file_path("castle.png", image=True)
        self.image = pygame.image.load(fp).convert()
        self.image = pygame.transform.scale(self.image,(2*TERRAIN,2*TERRAIN))
        self.image.set_colorkey(self.color.green)
        self.rect = self.image.get_rect()

    def activate(self):
        '''
        a function to make the castle active (captured)
        Parameters:
            None
        Returns:
            None
        '''
        self.active = True

    def deactivate(self):
        '''
        a function to deactivate the castle (not-captured)
        Parameters:
            None
        Returns:
            None
        '''
        self.active = False

    def set(self,pos):
        '''
        a function to set the coordinates of the castle
        Parameters:
            None
        Returns:
            None
        '''
        (x,y) = pos.get()
        self.rect.x = x
        self.rect.y = y

    def get(self):
        '''
        a function that gets the position of the castle
        Parameters:
            None
        Returns:
            tuple (x,y)
        '''
        return (self.rect.x, self.rect.y)

    def draw(self,surface):
        '''
        a function to draw the castle to the screen
        Parameters:
            surface: the screen to draw upon
        Returns:
            None
        '''
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)

    def conflict(self,pos):
        '''
        a function to check if the position conflicts with a castle
        Parameters:
            pos: the position to check (point)
        Returns:
            True if the position conflicts with the castle
            False otherwise
        '''
        (x,y) = pos.get()
        x_cond = self.rect.x < x and self.rect.x + 2 * TERRAIN > x
        y_cond = self.rect.y < y and self.rect.y + 2 * TERRAIN > y
        print("x {0} and y {1}".format(x_cond, y_cond))
        print("y {0}  y2 {1}".format(y, self.rect.y))
        conflicting = False
        if x_cond and y_cond:
            conflicting  = True
        return conflicting