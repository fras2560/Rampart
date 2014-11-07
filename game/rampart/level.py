'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 10/27/2014
@note: A level of rampart
'''

import logging
from graph import Graph
from graph.node import Node
from rampart.config import TERRAIN_TO_FILE, NODE_SIZE, CANNON, CANBUILD, BLOCK
class Level():
    def __init__(self, file_path, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger=logger
        self.logger.info("Loading Level" )
        with open(file_path) as f:
            lines = f.read().split("\n")
            dimensions = lines[0]
            row,column = self.parse_dimensions(dimensions)
            self.rows = row
            self.columns = column
            self.graph = Graph(row, column, self.logger)
            cond1 = len(lines[1:]) == row or len(lines[1:]) - 1 == row 
            assert cond1 ,'File has mismatching dimensions'
            r = 0
            for line in lines[1:]:
                if line != "":
                    nodes = line.split(",")
                    cond2 = len(nodes) == column 
                    assert cond2, 'File has mismatching dimensions'
                    c = 0
                    for node in nodes:
                        self.graph.set_node(r, c,
                                            Node(string_object=node, logger=self.logger))
                        c += 1
                r += 1
        self.logger.info("Done loading level")

    def save(self, file_path):
        '''
        a method to save the level to a specific file
        Parameters:
            file_path: where to save the file (os.path)
        Returns:
            None
        '''
        self.logger.info("Saving file %s" % file_path)
        with open(file_path, 'w') as f:
            f.write(str(self.rows) + 'X' + str(self.columns) + '\n')
            for row in range(0, self.rows):
                line = []
                for node in self.graph.iterate(row):
                    line.append(str(node))
                self.logger.debug(line)
                f.write(",".join(line) + '\n')
        self.logger.info("Done Saving file %s" % file_path)
        return

    def parse_dimensions(self, dimensions):
        '''
        a method to parse the dimensions string
        Parameters:
            dimensions: the dimensions (string)
        Returns:
            row: the number of nodes in each row (int)
            column: the number of node in each column (int)
        '''
        self.logger.debug(dimensions)
        dimensions = dimensions.split("X")
        self.logger.debug(dimensions)
        assert len(dimensions) == 2, 'Invalid Dimensions of file'
        row = int(dimensions[0])
        column = int(dimensions[1])
        return (row, column)

    def draw(self, surface):
        '''
        a method that draws the level
        Parameters:
            surface: the pygame display screen (surface)
        Returns:
            None
        '''
        self.graph.draw(surface)

    def update_node(self,x, y, terrain, player=None):
        '''
        a method that given the (x,y) determines updates the node at
        that position to given terrain type
        Parameters:
            x: the x position on the screen (int)
            y: the y position on the screen (int)
            terrain: the terrain type (int)
        Returns:
            None
        '''
        x = x - x % NODE_SIZE
        y = y -  y % NODE_SIZE
        n = Node(x, y, terrain, player=player)
        row = y // NODE_SIZE
        column = x // NODE_SIZE
        self.graph.set_node(row, column, n)
        return

    def add_cannon(self, x, y, player):
        '''
        a method to add a cannon to the level and the player
        Parameters:
            x: the x position (int)
            y: the y position (int)
            player: the player cannon (player)
        Returns:
            True if cannon was added
            False otherwise
        '''
        x = x - x % NODE_SIZE
        y = y -  y % NODE_SIZE
        add = True
        try:
            cannon = Node(x, y, CANNON, player=player.get_id())
            row = y // NODE_SIZE
            column = x // NODE_SIZE
            node = self.graph.get_node(row, column)
            if node.get_type() not in CANBUILD:
                add = False
        except:
            add = False
        if add:
            self.graph.set_node(row, column, cannon)
            player.add_cannon(cannon)
        return add

    def add_piece(self, player):
        '''
        a method used to add the piece of the player to the level
        Parameters:
            piece: the building piece to add (Piece)
        Returns:
            True if able to add piece, False otherwise (boolean)
        '''
        added = False
        # check if able to add piece
        valid = True
        piece = player.get_piece()
        for point in piece.return_points():
            column = point[0] 
            row = point[1]
            column = column // NODE_SIZE
            row = row // NODE_SIZE
            try:
                node = self.graph.get_node(row, column)
                if node.get_type() not in CANBUILD:
                    valid = False
                    break
            except AssertionError:
                valid = False
                break
        self.logger.debug(" Able to add piece: %s" % valid)
        if valid:
            added = True
            for point in piece.return_points():
                column = point[0]
                row = point[1]
                x = column - column % NODE_SIZE
                y = row - row % NODE_SIZE
                column = column // NODE_SIZE
                row = row // NODE_SIZE
                add_node = Node(x=x, y=y,
                                terrain=BLOCK, player=player.get_id())
                self.graph.set_node(row, column, add_node)
        return added

import unittest
import os
import pygame
from rampart.config import WATER
from rampart.player import Player
from rampart.piece import Piece

class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        directory = os.path.dirname(os.getcwd())
        self.directory = os.path.join(directory, 'levels')
        self.fp = os.path.join(self.directory, 'test.txt')
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        self.level = Level(self.fp, logger=self.logger)
        self.fp_save = os.path.join(self.directory, 'output.txt')

    def tearDown(self):
        if os.path.isfile(self.fp_save):
            os.remove(self.fp_save)

    def testDraw(self):
        self.level.draw(self.screen)

    def testSave(self):
        self.level.save(self.fp_save)
        self.level = Level(self.fp_save)

    def testParseDimensions(self):
        dimensions = '3X4'
        row,column = self.level.parse_dimensions(dimensions)
        self.assertEqual(row, 3)
        self.assertEqual(column, 4)

    def testUpdateNode(self):
        self.level.update_node(0, 0, WATER)
        result = self.level.graph.get_node(0, 0).get_type()
        self.assertEqual(result, WATER)
        self.level.update_node(10, 0, WATER)
        result = self.level.graph.get_node(0, 1).get_type()
        self.assertEqual(result, WATER)
        self.level.update_node(0, 10, WATER)
        result = self.level.graph.get_node(1, 0).get_type()
        self.assertEqual(result, WATER)

    def testAddPieceSimple(self):
        piece = Piece()
        piece._O_piece()
        player = Player()
        player.piece = piece
        added = self.level.add_piece(player)
        self.assertEqual(added, True)
        added = self.level.add_piece(player)
        self.assertEqual(added, False)

    def testAddPiece(self):
        fp = os.path.join(self.directory, "piece-test.txt")
        self.level = Level(fp, logger=self.logger)
        piece = Piece()
        player = Player()
        piece._O_piece()
        player.piece = piece
        added = self.level.add_piece(player)
        self.assertEqual(added, True)
        piece.translate(NODE_SIZE, 0)
        added = self.level.add_piece(player)
        self.assertEqual(added, False)
        self.level.add_cannon(2*NODE_SIZE, 2*NODE_SIZE, player)
        piece.translate(0, NODE_SIZE)
        added = self.level.add_piece(player)
        self.assertEqual(added, False)
        piece.translate(NODE_SIZE, NODE_SIZE)
        added = self.level.add_piece(player)
        self.assertEqual(added, False)
        piece.translate(NODE_SIZE, NODE_SIZE)
        added = self.level.add_piece(player)
        self.assertEqual(added, True)

    def testAddCannon(self):
        player = Player()
        added = self.level.add_cannon(-10, -10, player)
        self.assertEqual(added, False)
        added = self.level.add_cannon(0, -10, player)
        self.assertEqual(added, False)
        added = self.level.add_cannon(-10, 0, player)
        self.assertEqual(added, False)
        added = self.level.add_cannon(300, 0, player)
        self.assertEqual(added, False)
        added = self.level.add_cannon(0, 300, player)
        self.assertEqual(added, False)
        added = self.level.add_cannon(0, 0, player)
        self.assertEqual(added, True)
        added = self.level.add_cannon(0, 0, player)
        self.assertEqual(added, False)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()