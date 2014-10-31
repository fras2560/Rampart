'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
from point import Point
import os
import pygame
import helper
from color import Color

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = Color()
        self.stage = 1
        self.image = pygame.image.load(helper.file_path("explosion_1.png", image=True)).convert()
        self.image.set_colorkey(self.color.black)
        self.finished = False
        self.radius = 5
        self.rect = self.image.get_rect()

    def set(self, point):
        '''
        a function to set the point of the explosion
        Parameters:
            point: the point of the explosion
        Returns:
            None
        '''
        self.stage = 1
        self.finished = False
        (x,y) = point.get()
        self.x = x
        self.y = y

    def load_image(self):
        '''
        a function to load the current image of the explosion
        Parameters:
            None
        Returns:
            None
        '''
        fp = helper.file_path("explosion_"+str(self.stage)+".png", image=True)
        self.image = pygame.image.load(fp).convert()
        self.image.set_colorkey(self.color.black)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        '''
        a function that updates the explosion sequence
        Parameters:
            None
        Returns:
            None
        '''
        if self.stage == 1:
            self.load_image()
        elif self. stage == 2:
            self.load_image()
        elif self.stage == 3:
            self.load_image()
        elif self.stage == 4:
            self.load_image()
        elif self.stage == 5:
            self.load_image()
        elif self.stage >= 6:
            self.load_image()
            self.finished = True
        self.stage += 1

    def draw(self,surface):
        '''
        a function to draw the explosion
        Parameters:
            surface: the surface to draw on
        '''
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)
