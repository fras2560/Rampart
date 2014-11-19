'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import pygame
import helper
from color import Color
from rampart.config import EXPLOSIONS
class Explosion(pygame.sprite.Sprite):
    def __init__(self, sounds=None):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.rects = []
        self.color = Color()
        for explosion in EXPLOSIONS:
            fp = helper.file_path(explosion, image=True)
            image = pygame.image.load(fp).convert()
            image.set_colorkey(self.color.black)
            self.images.append(image)
            self.rects.append(image.get_rect())
        self.stage = 1
        self.finished = False
        self.radius = 5
        self.x = 0 
        self.y = 0

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

    def update(self):
        '''
        a function that updates the explosion sequence
        Parameters:
            None
        Returns:
            None
        '''
        if self.stage >= 6:
            self.finished = True
        self.stage += 1

    def draw(self,surface):
        '''
        a function to draw the explosion
        Parameters:
            surface: the surface to draw on
        '''
        surface_blit = surface.blit
        if self.stage < len(self.images):
            self.rects[self.stage].x = self.x
            self.rects[self.stage].y = self.y
            surface_blit(self.images[self.stage], self.rects[self.stage])

import unittest
from rampart.point import Point
class testExplosion(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Test Explosion Object")
        self.explosion = Explosion()
        self.p = Point()
        self.p.set(x=10, y=10)

    def tearDown(self):
        pygame.quit()

    def testUpdate(self):
        i = 1
        self.assertEqual(self.explosion.stage, i)
        while not self.explosion.finished:
            self.explosion.update()
            i += 1
            self.assertEqual(self.explosion.stage, i)
        self.assertEqual(self.explosion.stage, 7)

    def testSetPoint(self):
        self.explosion.set(self.p)
        self.assertEqual(self.explosion.x, 10)
        self.assertEqual(self.explosion.y, 10)

    def testDraw(self):
        self.explosion.set(self.p)
        while not self.explosion.finished:
            self.explosion.draw(self.screen)
            self.explosion.update()