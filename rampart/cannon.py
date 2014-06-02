'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
from cannonball import Cannonball
from point import Point
import helper
import pygame
from color import Color
from config import TERRAIN

class Cannon(pygame.sprite.Sprite):
    def __init__(self):
        self.ball = Cannonball()
        self.position = Point()
        self.color = Color()
        fp = helper.file_path("cannon.png", image=True)
        self.image = pygame.image.load(fp).convert()
        self.image = pygame.transform.scale(self.image, (TERRAIN,TERRAIN))
        self.image.set_colorkey(self.color.white)
        self.rect = self.image.get_rect()
        self.active = True

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def set(self,p):
        '''
        a function that sets the position of the cannon
        Parameters:
            p: the point of the cannon
        Returns:
            None
        '''
        self.position = p
        (x,y) = p.get()
        self.rect.x = x
        self.rect.y = y

    def get(self):
        '''
        a function that sets the position of the cannon
        Parameters:
            None
        Returns:
            (x1,y1): the x and y position
        '''
        return self.position.get()

    def shoot(self,point):
        '''
        a function to shoot the cannonball if ready
        Parameters:
            point: the point to aim the cannonball at
        Returns:
            True if cannonball was shot
            False otherwise
        '''
        shot = False
        if not self.ball.in_air() and self.active:
            self.ball.reset()
            self.ball.set(self.position, point)
            shot = True
        return shot

    def update(self):
        '''
        a function that updates the cannon and its cannonball
        '''
        if self.ball.in_air():
            self.ball.update()

    def draw(self, surface):
        '''
        a function to draw the cannon
        Parameters:
            None
        Returns:
            None
        '''
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)
        if self.ball.in_air():
            self.ball.draw(surface)

    def conflict(self,pos):
        '''
        a function to check if the cannon conflicts with position given
        Parameters:
            pos: the position to check (point)
        Returns:
            True if conflicts
            False otherwise
        '''
        (x,y)  = pos.get()
        x_cond = self.rect.x >= x and self.rect.x + TERRAIN <= x 
        y_cond = self.rect.y >= y and self.rect.y + TERRAIN <= y
        conflicting = False
        if x_cond and y_cond:
            conflicting = True
        return conflicting