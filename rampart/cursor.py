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

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = Color()
        self.image = pygame.image.load(helper.file_path("cursor.png", image=True)).convert()
        self.image.set_colorkey(self.color.black)
        self.rect = self.image.get_rect()
    
    def set(self, point):
        (x,y) = point.get()
        self.rect.x = x
        self.rect.y = y
    
    def get(self):
        return (self.rect.x,self.rect.y)
    
    def move(self,horizontal=0,vertical=0):
        self.rect.x += horizontal
        self.rect.y += vertical

    def update(self):
        pass

    def draw(self,surface):
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)
