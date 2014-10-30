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
from rampart.config import TERRAIN, TYPES
from rampart.color import Color
import logging

'''
-------------------------------------------------------------------------------
Node Class
-------------------------------------------------------------------------------
'''

class Node(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file, terrain, logger=None):
        '''
        Parameters:
            x: the initial position of the x co-ordinate (int >= 0)
            y: the initial position of the y co-ordinate (int >= 0 )
            image_file: name of the image file 
                        in the assets/image directory (string)
            terrain: the type of terrain the node is (type in CONFIG)
        '''
        assert x >= 0, 'Node (x < 0) not initialized properly'
        assert y >= 0, 'Node (y < 0) not initialized properly'
        assert terrain in TYPES, ' Node given non-valid type'
        self.color = Color()
        fp = file_path(image_file, image=True)
        self.image = pygame.image.load(fp).convert()
        self.image = pygame.transform.scale(self.image, (TERRAIN, TERRAIN))
        self.image.set_colorkey(self.color.white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = terrain
        self.painted = False
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger=logger

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
        self.logger.debug("Drawing Node")
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)

    def get_type(self):
        '''
        a method that gets type of terrain of the node
        Parameters:
            None
        Returns:
            self.type: the type of terrain (int)
        '''
        return self.type

    def paint(self):
        '''
        a method that paints the node
        Parameters:
            None
        Returns:
            None
        '''
        self.painted = True

    def unpaint(self):
        '''
        a method that remove paint of a node
        Parameters:
            None
        Returns:
            None
        '''
        self.painted = False

    def is_painted(self):
        '''
        a method use to see if the node is_painted
        Parameters:
            None
        Returns:
            self.painted: a boolean for whether the node is painted or not
        '''
        return self.painted

'''
-------------------------------------------------------------------------------
Unittest Imports
-------------------------------------------------------------------------------
'''
import unittest
from rampart.config import SIZE, CANNON
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
        self.f = 'cannon.png'
        self.node = Node(10, 10, self.f, CANNON )

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

    def testFailedInitialize(self):
        try:
            self.node = Node(-1, -1, self.f, CANNON)
            self.assertEqual(True, False, "Should throw exception (x < 0)")
        except AssertionError:
            pass
        try:
            self.node = Node(0, -1, self.f, CANNON)
            self.assertEqual(True, False, "Should throw exception (x < 0)")
        except AssertionError:
            pass
        try:
            self.node = Node(0, -1, self.f, len(TYPES)*10)
            self.assertEqual(True, False,
                             "Should throw exception (non-valid terrain)")
        except AssertionError:
            pass
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()