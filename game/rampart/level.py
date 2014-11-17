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
from rampart.config import NODE_SIZE, CANNON, CANBUILD, BLOCK, TERRAIN_TO_FILE
from rampart.config import BACKGROUND, CASTLE, DESTROYED, GRASS
from graph.terrain import Terrain
import sys

class Level():
    def __init__(self, file_path, logger=None, testing=False):
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger=logger
        self.logger.info("Loading Level" )
        self.terrain = Terrain(TERRAIN_TO_FILE, NODE_SIZE, BACKGROUND)
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
                        n = Node(string_object=node,
                                  images=self.terrain,
                                  logger=self.logger)
                        self.graph.set_node(r, c, n)
                        c += 1
                r += 1
        self.logger.info("Done loading level")
        if not testing:
            sys.setrecursionlimit(self.graph.columns * self.graph.rows)

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
            player: the player the node belongs to (Player)
        Returns:
            None
        '''
        x = x - x % NODE_SIZE
        y = y -  y % NODE_SIZE
        if player is not None:
            player = player.get_id()
        n = Node(x=x, y=y, terrain=terrain, player=player, images=self.terrain)
        row = y // NODE_SIZE
        column = x // NODE_SIZE
        self.graph.set_node(row, column, n)
        return

    def add_castle(self, x, y, player):
        '''
        a method to add a castle
        Parameters:
            x: the position (int)
            y: the y position (int)
            player: the player who the castle belongs to (player)
        Returns:
            added: True if able to add castle False otherwise (boolean)
        '''
        x = x - x % NODE_SIZE
        y = y -y % NODE_SIZE
        row = y // NODE_SIZE
        column = x // NODE_SIZE
        added = False
        row_cond = row > 2 and row < self.rows - 2
        col_cond = column > 2 and column < self.columns - 2
        outer_edge = row_cond and col_cond
        if player is not None:
            p = player.get_id()
            self.logger.info("Player's Castle: %i" % p)
        self.logger.info("Outer edge condition: %s" % outer_edge)
        if player is not None and outer_edge and self.check_castle(row, column):
            nodes = []
            i = 0
            for (r, c) in castle_spot(row, column):
                nodes.append(Node(x=c*NODE_SIZE, y=r*NODE_SIZE, terrain=CASTLE,
                            player=p, images=self.terrain))
                self.graph.set_node(r, c, nodes[i])
                i += 1
            added = True
            player.add_castle(nodes[0])
        return added

    def check_castle(self, row, column):
        '''
        a method to check if can add the castle to that spot
        Parameters:
            row: the row index (int)
            column: the column index (int)
        Return:
            valid: True if castle is valid, False otherwise (boolean)
        '''
        valid = True
        for (r,c) in castle_spot(row, column):
            try:
                node_id = self.graph.get_node_id(r, c)
                if not self.graph.available(node_id):
                    self.logger.info("Node not available: %d" % node_id)
                    valid = False
            except:
                self.logger.info("Invalid node id")
                valid = False
            if not valid:
                break
        self.logger.info("Add castle: %s" % valid)
        return valid

    def add_cannon(self, x, y, player, game=True):
        '''
        a method to add a cannon to the level and the player
        Parameters:
            x: the x position (int)
            y: the y position (int)
            player: the player cannon (player)
            game: True if part of game, False if want to add manually
        Returns:
            True if cannon was added
            False otherwise
        '''
        x = x - x % NODE_SIZE
        y = y -  y % NODE_SIZE
        add = True
        try:
            cannon = Node(x=x, y=y, terrain=CANNON,
                          images=self.terrain,player=player.get_id())
            row = y // NODE_SIZE
            column = x // NODE_SIZE
            node = self.graph.get_node(row, column)
            if node.get_type() not in CANBUILD:
                add = False
            if game and node.is_painted():
                add = False
        except:
            add = False
        if add:
            self.graph.set_node(row, column, cannon)
            player.add_cannon(cannon)
        return add

    def destroy_node(self, x, y):
        '''
        a method that destroys the node
        Parameters:
            x: the x position (int)
            y: the y position (int)
        Returns:
            None
        '''
        row = (y) // NODE_SIZE
        column = (x) // NODE_SIZE
        self.graph.destroy_node(row, column)

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
                add_node = Node(x=x, y=y, terrain=BLOCK,
                                images=self.terrain, player=player.get_id())
                self.graph.set_node(row, column, add_node)
        return added

    def update(self):
        '''
        a method to update the level
        Parameters:
            None:
        Returns:
            None
        '''
        self.graph.paint()

    def add_players_castles(self, player):
        '''
        a method that takes the levels castles and adds them to the player
        Parameters:
            player: the player to add to (Player)
        Returns:
            None
        '''
        pid = player.get_id()
        self.logger.info("Adding Castles to player: %d" % pid)
        for node in self.graph.iterate():
            right_player = node.get_player() == pid
            if node.get_type() == CASTLE and right_player:
                player.add_castle(node)
        return

    def cleanup(self):
        '''
        a method that cleanup the level of all destroyed squares
        Parameters:
            None
        Returns:
            None
        '''
        for node in self.graph.iterate():
            if node.get_state() == DESTROYED:
                (x, y) = node.get()
                self.update_node(x, y, GRASS)

from rampart.config import CASTLE_SPOTS
def castle_spot(row, column):
    for (r,c) in CASTLE_SPOTS:
        yield (row+r, column+c)

import unittest
import os
import pygame
from rampart.config import WATER, NORMAL
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
        self.level = Level(self.fp, logger=self.logger, testing=True)
        self.fp_save = os.path.join(self.directory, 'output.txt')

    def tearDown(self):
        if os.path.isfile(self.fp_save):
            os.remove(self.fp_save)

    def testDraw(self):
        self.level.draw(self.screen)

    def testSave(self):
        self.level.save(self.fp_save)
        self.level = Level(self.fp_save, testing=True)

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
        self.level = Level(fp, logger=self.logger, testing=True)
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
        self.assertEqual(added, True)
        piece.translate(NODE_SIZE, NODE_SIZE)
        added = self.level.add_piece(player)
        self.assertEqual(added, False)

    def testAddCannonSimple(self):
        player = Player()
        added = self.level.add_cannon(-10, -10, player, game=False)
        self.assertEqual(added, False)
        added = self.level.add_cannon(0, -10, player, game=False)
        self.assertEqual(added, False)
        added = self.level.add_cannon(-10, 0, player, game=False)
        self.assertEqual(added, False)
        added = self.level.add_cannon(300, 0, player, game=False)
        self.assertEqual(added, False)
        added = self.level.add_cannon(0, 300, player, game=False)
        self.assertEqual(added, False)
        added = self.level.add_cannon(0, 0, player, game=False)
        self.assertEqual(added, True)
        added = self.level.add_cannon(0, 0, player, game=False)
        self.assertEqual(added, False)

    def testAddCannonComplex(self):
        # not surronded by wall
        player = Player()
        added = self.level.add_cannon(10, 10, player)
        self.assertEqual(added, False)
        # build the wall around it
        self.level.update_node(0, 0, BLOCK)
        self.level.update_node(10, 0, BLOCK)
        self.level.update_node(20, 0, BLOCK)
        self.level.update_node(0, 10, BLOCK)
        # self.level.update_node(10, 10, BLOCK)
        self.level.update_node(20, 10, BLOCK)
        self.level.update_node(0, 20, BLOCK)
        self.level.update_node(10, 20, BLOCK)
        self.level.update_node(20, 20, BLOCK)
        self.level.update()
        added = self.level.add_cannon(10, 10, player)
        self.assertEqual(added, True)

    def testCheckCastle(self):
        result = self.level.check_castle(0, 0)
        self.assertEqual(result, True)
        self.level.update_node(0, 0, BLOCK)
        result = self.level.check_castle(0, 0)
        self.assertEqual(result, False)
        self.level.update_node(10, 0, WATER)
        result = self.level.check_castle(0, 2)
        self.assertEqual(result, False)
        result = self.level.check_castle(2, 2)
        self.assertEqual(result, False)

    def testAddCastle(self):
        fp = os.path.join(self.directory, 'castle-test.txt')
        self.level = Level(fp, logger=self.logger, testing=True)
        player = Player()
        added = self.level.add_castle(0, 0, player)
        self.assertEqual(added, False)
        added = self.level.add_castle(10, 0, player)
        self.assertEqual(added, False)
        added = self.level.add_castle(0, 10, player)
        self.assertEqual(added, False)
        added = self.level.add_castle(10, 10, player)
        self.assertEqual(added, False)
        added = self.level.add_castle(10, 20, player)
        self.assertEqual(added, False)
        added = self.level.add_castle(20, 20, player)
        self.assertEqual(added, False)
        added = self.level.add_castle(30, 30, player)
        self.assertEqual(added, True)
        added = self.level.add_castle(30, 30, player)
        self.assertEqual(added, False)

    def testCleanup(self):
        player = Player()
        self.level.update_node(0, 0, BLOCK, player)
        cell = self.level.graph.get_node(0, 0)
        before = cell.get_type()
        self.level.destroy_node(0, 0)
        self.level.cleanup()
        cell = self.level.graph.get_node(0, 0)
        self.assertNotEqual(cell.get_type(), before)
        self.assertEqual(cell.get_type(), GRASS)
        self.assertEqual(cell.get_state(), NORMAL)

    def testDestroyNode(self):
        player = Player()
        self.level.update_node(0, 0, BLOCK, player)
        cell = self.level.graph.get_node(0, 0)
        before = cell.get_state()
        self.level.destroy_node(0, 0)
        cell = self.level.graph.get_node(0, 0)
        after = cell.get_state()
        self.assertNotEqual(after, before)
        self.assertEqual(after, DESTROYED)
if __name__ == "__main__":
    unittest.main()