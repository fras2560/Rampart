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
        (x,y) = point.get()
        self.x = x
        self.y = y

    def load_image(self):
        fp = helper.file_path("explosion_"+str(self.stage)+".png", image=True)
        self.image = pygame.image.load(fp).convert()
        self.image.set_colorkey(self.color.black)
        self.pos = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
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
        elif self.stage == 6:
            self.load_image()
            self.finished = True
        self.stage += 1