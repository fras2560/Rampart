'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import pygame
import rampart.helper as helper
from rampart.color import Color

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = Color()
        self.image = pygame.image.load(helper.file_path("cursor.png", image=True)).convert()
        self.image.set_colorkey(self.color.black)
        self.rect = self.image.get_rect()
    
    def set(self, point):
        '''
        a function that sets the point of the cursor
        Parameters:
            point: the point of the cursor
        Returns:
            None
        '''
        (x,y) = point.get()
        self.rect.x = x
        self.rect.y = y
    
    def get(self):
        '''
        a function to get the position of the cursor
        Parameters:
            None
        Returns
            (x,y): the x and y position (tuple)
        '''
        return (self.rect.x, self.rect.y)
    
    def move(self, horizontal=0, vertical=0):
        '''
        a function to move the cursor
        Parameters:
            horizontal: the movement in the x axis
            vertical: the movement in the y axis
        Returns:
            None
        '''
        self.rect.x += horizontal
        self.rect.y += vertical

    def update(self):
        '''
        a function to update the cursor
        Parameters:
            None
        Returns:
            None
        '''
        pass

    def draw(self, surface):
        '''
        a function to draw the cursor
        Parameters:
            surface: the surface to draw on
        '''
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)
