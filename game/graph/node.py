'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: Oct 27, 2014
@note: The main of rampart
'''

'''
-------------------------------------------------------------------------------
Imports
-------------------------------------------------------------------------------
'''
import pygame
from rampart.helper import file_path
from rampart.config import TERRAIN
from rampart.color import Color
'''
-------------------------------------------------------------------------------
Node Class
-------------------------------------------------------------------------------
'''

class Node(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        self.color = Color()
        fp = file_path(image_file, image=True)
        self.image = pygame.image.load(fp).convert()
        self.image = pygame.transform.scale(self.image, (TERRAIN, TERRAIN))
        self.image.set_colorkey(self.color.white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x=None, y=None):
        '''
        a method to update the node position (in pixels)
        Parameters:
            x: an integer value (int >= 0)
            y: an integer value (int >= 0)
        Returns:
            None
        '''
        if x is not None:
            assert x >= 0, 'Node->update not given positive value for x'
            self.rect.x = x
        if y is not None:
            assert y >= 0, 'Node->update not given positive value for y'
            self.rect.y = y

    def draw(self, surface):
        '''
        a method to draw the node on the surface
        Parameters:
            surface: the pygame display surface (display)
        Returns:
            None
        '''
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)

'''
-------------------------------------------------------------------------------
Unittest Imports
-------------------------------------------------------------------------------
'''
import unittest
from rampart.config import SIZE
'''
-------------------------------------------------------------------------------
Unittests for Node
-------------------------------------------------------------------------------
'''
class Test(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Node Object")
        self.color = Color()
        self.screen.fill(self.color.white)
        f = 'cannon.png'
        self.node = Node(10, 10, f)

    def tearDown(self):
        pygame.quit()

    def testDraw(self):
        # just to see if image is actually drawn
        self.node.draw(self.screen)

    def testUpdate(self):
        # only change x
        before_x = self.node.rect.x
        before_y = self.node.rect.y
        change = 0
        self.node.update(x=change)
        result_x = self.node.rect.x
        result_y = self.node.rect.y
        self.assertNotEqual(before_x, result_x)
        self.assertEqual(before_y, result_y)
        self.assertEqual(change, result_x)
        # only change y
        before_x = self.node.rect.x
        before_y = self.node.rect.y
        change = 5
        self.node.update(y=change)
        result_x = self.node.rect.x
        result_y = self.node.rect.y
        self.assertNotEqual(before_y, result_y)
        self.assertEqual(before_x, result_x)
        self.assertEqual(change, result_y)
        # change both x and y
        before_x = self.node.rect.x
        before_y = self.node.rect.y
        change = 15
        self.node.update(x=change, y=change)
        result_x = self.node.rect.x
        result_y = self.node.rect.y
        self.assertEqual(change, result_x)
        self.assertEqual(change, result_y)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()