'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: The grass, water terrain objects
'''
import helper
import pygame
from color import Color
class Terrain(pygame.sprite.Sprite):
    def __init__(self,file):
        self.color = Color()
        fp = helper.file_path(file, image=True)
        self.image = pygame.image.load(fp).convert()
        self.image.set_colorkey(self.color.white)
        self.rect = self.image.get_rect()

    def update(self,x=None, y=None):
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y

    def draw(self,surface):
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)