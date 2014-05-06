'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used as the castle for rampart game
'''
import pygame
import helper
from color import Color

class Castle(pygame.sprite.Sprite):
    def __init__(self):
        self.active = False
        self.color = Color()
        fp = helper.file_path("castle.png", image=True)
        self.image = pygame.image.load(fp).convert()
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