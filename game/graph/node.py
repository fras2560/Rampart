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
from rampart.config import TERRAIN, TYPES, NONPLAYER, TERRAIN_TO_FILE
from rampart.config import NORMAL, NODE_SIZE
from rampart.color import Color
import logging

'''
-------------------------------------------------------------------------------
Node Class
-------------------------------------------------------------------------------
'''

class Node(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, terrain=None,
                 logger=None, string_object=None, player=None):
        '''
        Parameters:
            x: the initial position of the x co-ordinate (int >= 0)
            y: the initial position of the y co-ordinate (int >= 0 )
            image_file: name of the image file 
                        in the assets/image directory (string)
            terrain: the type of terrain the node is (type in CONFIG)
            logger: the logger of the node object (logger)
            string_object: the string representing the obejct (string)
            player: the player id (int)
        Ways to Initialize:
            Node(x=int, y=int, terrain=int)
            OR
            Node(string_object=string)
            logger is always an option argument
        '''
        if string_object is not None:
            terrain, x, y, player = self.parse_string(string_object)
        else:
            assert x is not None, 'Node not given x property'
            assert y is not None, 'Node not given y property'
            assert terrain is not None, 'Node not given terrain property'
        assert x >= 0, 'Node (x < 0) not initialized properly'
        assert y >= 0, 'Node (y < 0) not initialized properly'
        assert terrain in TYPES, ' Node given non-valid type'
        self.color = Color()
        image_files = TERRAIN_TO_FILE[terrain]
        self.images = []
        self.rects = []
        for f_type in image_files:
            images = []
            rects = []
            for f in f_type:
                fp = file_path(f, image=True)
                image = pygame.image.load(fp).convert()
                image = pygame.transform.scale(image, (TERRAIN, TERRAIN))
                image.set_colorkey(self.color.green)
                rect = image.get_rect()
                images.append(image)
                rects.append(rect)
            self.images.append(images)
            self.rects.append(rects)
        self.x = x
        self.y = y
        self.type = terrain
        self.painted = False
        self.state = NORMAL
        if player is None:
            player = NONPLAYER
        self.player = player
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger=logger

    def __str__(self):
        '''
        a method to take the object and turn into a string
        Parameters:
            None
        Returns:
            to_string: the string representing the object (string)
        '''
        to_string = str(self.get_type()) + ":"
        to_string += "x=" + str(self.x)
        to_string += "y=" + str(self.y)
        to_string += 'player='+str(self.player)
        return to_string

    def parse_string(self, string_object):
        '''
        a method to parse the string into the object parts
        Parameters:
            string_object: the string representing the object (string)
        Returns:
            terrain: the terrain type (int)
            x: the x position (int)
            y: the y position (int)
            player: wich player the node belons to (int)
        '''
        parts = string_object.split(":")
        assert len(parts) == 2, 'Node->parse_string: Invalid String'
        terrain = int(parts[0])
        parts = parts[1].split("y=")
        x = int(parts[0].replace("x=", ""))
        parts = parts[1].split("player=")
        y = int(parts[0])
        player = int(parts[1])
        return terrain, x, y, player

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
            self.x = x
        if y is not None:
            assert y >= 0, 'Node->update not given positive value for y'
            self.y = y

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
        row = self.x // NODE_SIZE
        column = self.y // NODE_SIZE
        odd = (row % 2 + column) % 2
        if odd == 1 and len(self.rects[self.state]) <= 1:
            odd = 0
        self.rects[self.state][odd].x = self.x
        self.rects[self.state][odd].y = self.y
        surface_blit(self.images[self.state][odd], self.rects[self.state][odd])

    def get_type(self):
        '''
        a method that gets type of terrain of the node
        Parameters:
            None
        Returns:
            self.type: the type of terrain (int)
        '''
        return self.type

    def get(self):
        '''
        a method that gets the position of the node
        Parameters:
            None
        Returns:
            (x,y): a tuple representing the position (int)
        '''
        return (self.x, self.y)

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

    def get_player(self):
        '''
        a method to the the player in which the node belongs to
        Parameters:
            None
        Returns:
            self.player: the id of the player (int)
        '''
        return self.player

'''
-------------------------------------------------------------------------------
Unittest Imports
-------------------------------------------------------------------------------
'''
import unittest
from rampart.config import SIZE, CANNON, GRASS
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
        self.node = Node(10, 10, CANNON )

    def tearDown(self):
        pygame.quit()

    def testDraw(self):
        # just to see if image is actually drawn
        self.node.draw(self.screen)

    def testUpdate(self):
        # only change x
        before_x = self.node.x
        before_y = self.node.y
        change = 0
        self.node.update(x=change)
        result_x = self.node.x
        result_y = self.node.y
        self.assertNotEqual(before_x, result_x)
        self.assertEqual(before_y, result_y)
        self.assertEqual(change, result_x)
        # only change y
        before_x = self.node.x
        before_y = self.node.y
        change = 5
        self.node.update(y=change)
        result_x = self.node.x
        result_y = self.node.y
        self.assertNotEqual(before_y, result_y)
        self.assertEqual(before_x, result_x)
        self.assertEqual(change, result_y)
        # change both x and y
        before_x = self.node.x
        before_y = self.node.y
        change = 15
        self.node.update(x=change, y=change)
        result_x = self.node.x
        result_y = self.node.y
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

    def testStrAndParseString(self):
        node_string = str(self.node)
        expect = '2:x=10y=10player=0'
        self.assertEqual(node_string, expect)
        expect = (2, 10, 10, 0)
        result = self.node.parse_string(node_string)
        self.assertEqual(result, expect)

    def testInitializeWithString(self):
        node_string = str(self.node)
        self.node = Node(string_object=node_string)
        self.assertEqual(node_string, str(self.node))

    def testImproperInitialize(self):
        try:
            self.node = Node(x='s')
            self.assertEqual(True, False, 'Exception should be thrown')
        except AssertionError:
            pass
        try:
            self.node = Node(x=1, y=2, terrain=5)
            self.assertEqual(True, False, 'Exception should be thrown')
        except AssertionError:
            pass
        try:
            self.node = Node(x=1, y=2, terrain=5)
            self.assertEqual(True, False, 'Exception should be thrown')
        except AssertionError:
            pass
        try:
            self.node = Node(x=1, y=2, terrain='s')
            self.assertEqual(True, False, 'Exception should be thrown')
        except AssertionError:
            pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()