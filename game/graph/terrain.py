'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 11/08/2014
@note: Holds all the terrain images
'''
import pygame
from rampart.helper import file_path
class Terrain():
    '''
    a class to hold all the terrain images and rects
    '''
    def __init__(self, terrain_to_files, terrain_size, color):
        '''
        Terrain()
        Parameters:
            terrain_to_files: a dictionary of the terrains, their states and 
                             images for each terrain state (dict)
            terrain_size: the size of the terrain (int)
            color: the color of the background (RR,GG,BB)
        '''
        self.images ={}
        self.rects = {}
        size = (terrain_size, terrain_size)
        for terrain in terrain_to_files:
            self.images[terrain] = []
            self.rects[terrain] = []
            for state in terrain_to_files[terrain]:
                images = []
                rects = []
                for pic in state:
                    fp = file_path(pic, image=True)
                    image = pygame.image.load(fp).convert()
                    image = pygame.transform.scale(image, size)
                    image.set_colorkey(color)
                    rect = image.get_rect()
                    images.append(image)
                    rects.append(rect)
                self.images[terrain].append(images)
                self.rects[terrain].append(rects)

    def get_image(self, terrain, state):
        return self.images[terrain][state]

    def get_rect(self, terrain, state):
        return self.rects[terrain][state]


import unittest
from rampart.config import TERRAIN_TO_FILE, NODE_SIZE, SIZE, TYPES
from rampart.config import NORMAL, DESTROYED, UNPAINTED

class TerrainTeser(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Node Object")
        self.terrain = Terrain(TERRAIN_TO_FILE, NODE_SIZE, ( 189,   0, 252))

    def tearDown(self):
        pass

    def testGetImage(self):
        states = [NORMAL, DESTROYED, UNPAINTED]
        for t in TYPES:
            for s in states:
                self.terrain.get_image(t, s)

    def testGetRect(self):
        states = [NORMAL, DESTROYED, UNPAINTED]
        for t in TYPES:
            for s in states:
                self.terrain.get_rect(t, s)

if __name__ == "__main__":
    unittest.main()
