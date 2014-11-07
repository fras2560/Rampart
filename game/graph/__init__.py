'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 10/27/2014
@note: A graph which holds the information of a rampart level
'''

'''
-------------------------------------------------------------------------------
Imports
-------------------------------------------------------------------------------
'''
import logging
import networkx as nx
from rampart.config import PAINTED, BLOCK

class Graph():
    def __init__(self, row, column, logger=None):
        '''
        Parameters:
            row: the number of nodes in a row (int > 0)
            column: the number of nodes in a column (int > 0)
        '''
        assert row > 0, 'Graph initialized with invalid row size (<= 0)'
        assert column > 0, 'Graph initialized with invalid column size (<= 0)'
        self.columns = column
        self.rows = row
        self.graph = nx.Graph()
        for y in range(0, row):
            for x in range(0, column):
                # add all nodes
                self.graph.add_node(self.get_node_id(x, y))
        # add all edges
        for node in self.graph.nodes():
            row,column = self.get_row_column(node)
            if row != (self.rows - 1):
                self.graph.add_edge(node, self.get_node_id(row + 1, column))
                if column != 0:
                    self.graph.add_edge(node, self.get_node_id(row + 1,
                                                               column - 1))
            if column != (self.columns - 1):
                self.graph.add_edge(node, self.get_node_id(row, column + 1))
            if column != (self.columns - 1) and row != (self.rows - 1):
                self.graph.add_edge(node, self.get_node_id(row + 1, column + 1))
        if logger is None:
            logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger=logger
        self.logger.info("Created a Graph %d X %d" % (self.rows, self.columns))

    def iterate(self, row=None):
        '''
        a method used to iterate through the graph nodes
        Parameters:
            row: if row is given only iterates on that row
        Yields:
            node: a graph node
        '''
        nodes = nx.get_node_attributes(self.graph, 'nodes')
        if row is None:
            for node in nodes:
                yield nodes[node]
        else:
            for c  in range(0, self.columns):
                yield nodes[self.get_node_id(row, c)]

    def get_node_id(self, row, column):
        '''
        a method the finds the node id for the (x,y) pair given
        Parameters:
            row: the row in which the node is located (int >= 0)
            column: the column in which the node is located (int >= 0)
        '''
        assert row >= 0, 'Graph->get_node_id: invalid row index (<0)'
        assert column >= 0, 'Graph->get_node_id: invalid column index (<0)'
        assert row < self.rows, 'Graph->get_node_id: invalid row index (>bound)'
        m = 'Graph->get_node_id: invalid column index (>bound)'
        assert column < self.columns, m
        node_id = column + self.columns * row
        return node_id

    def get_row_column(self, node_id):
        '''
        a method that finds the (row, column) from the node id
        Parameters:
            node_id: the node id (int >= 0)
        Returns:
            (row, column): a tuple of the row and column (int)
        '''
        assert node_id >= 0, 'Graph->get_row_column: invalid node_id (<0)'
        column = node_id % self.columns
        row = int((node_id - column) / self.columns)
        return (row, column)

    def set_node(self, row, column, node):
        '''
        a method that sets the node type of the graph
        Parameters:
            row: the row index (int >= 0)
            column: the column index (int >= 0)
            node: the node data structure (node)
        Returns:
            None
        '''
        values = {self.get_node_id(row, column): node}
        nx.set_node_attributes(self.graph, 'nodes', values)
        self.logger.info("Set (%d, %d) Node to type: %d"
                         %(row, column, node.get_type()))

    def update_node(self, row, column, x=None, y=None):
        '''
        a method that updates the position of the node
        Parameters:
            row: the row index (int >= 0)
            column: the column index (int >= 0)
            node: the node data structure (node)
        Returns:
            None
        '''
        nodes = nx.get_node_attributes(self.graph, 'nodes')
        nodes[self.get_node_id(row, column)].update(x=x, y=y)
        self.logger.info("Updated Position of Node (%d, %d)"
                         %(row,column))
        return

    def get_node(self, row, column):
        '''
        a method that updates the position of the node
        Parameters:
            row: the row index (int >= 0)
            column: the column index (int >= 0)
        Returns:
            : the node at the given index (node)
        '''
        nodes = nx.get_node_attributes(self.graph, 'nodes')
        return nodes[self.get_node_id(row, column)]

    def draw(self, surface):
        '''
        a method that draws the graph
        Parameters:
            surface: the pygame display surface (display)
        Returns:
            None
        '''
        nodes = nx.get_node_attributes(self.graph, 'nodes')
        for node in nodes:
            nodes[node].draw(surface)

    def paint(self):
        '''
        a method use to paint the nodes starting a top left and moving 
        to each nodes neighbors unless blocked by a block
        Parameters:
            None
        Returns:
            None
        '''
        # reset to not painted
        nodes = nx.get_node_attributes(self.graph, 'nodes')
        assert len(nodes) > 0, 'Graph not initialized with nodes'
        for index in range(0, len(nodes)):
            nodes[index].unpaint()
        self.nodes = nodes
        self.paint_aux(0)

    def paint_aux(self, node_id):
        '''
        a aux method used to paint all the nodes
        Parameters:
            node_id: the current node to paint
        Returns:
            None
        '''
        if self.nodes[node_id].get_type() != BLOCK:
            self.nodes[node_id].paint()
            self.logger.debug("Painted Node_id %d"  %node_id)
            for neighbor in self.graph.neighbors(node_id):
                cond1 = not self.nodes[neighbor].is_painted()
                cond2 = self.nodes[neighbor].get_type () != BLOCK
                if cond1 and cond2 :
                    self.paint_aux(neighbor)
        return

import unittest
from graph.node import Node
from rampart.config import GRASS
import pygame
class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        self.rows = 3
        self.columns = 3
        self.g = Graph(self.rows, self.columns, logger=logger)
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))

    def tearDown(self):
        pygame.quit()

    def testConstructor(self):
        result = len(self.g.graph.nodes())
        self.assertEqual(result, self.rows * self.columns)
        expect = {0:[1, 3, 4],
                  1:[0, 2, 3, 4, 5],
                  2:[1, 4, 5],
                  3:[0, 1, 4, 6, 7],
                  4:[0, 1, 2, 3, 5, 6, 7, 8],
                  5:[1, 2, 4, 7, 8],
                  6:[3, 4, 7],
                  7:[3, 4, 5, 6, 8],
                  8:[4, 5, 7],
                  }
        for node in self.g.graph.nodes():
            self.assertEqual(expect[node],
                             sorted(self.g.graph.neighbors(node)))

    def testGetNodeId(self):
        try:
            self.g.get_node_id(-1, -1)
            self.assertEqual(True, False,
                             'get_node_id should raise exception (x<0)')
        except AssertionError:
            pass
        try:
            self.g.get_node_id(0, -1)
            self.assertEqual(True, False,
                             'get_node_id should raise exception (y<0)')
        except AssertionError:
            pass
        try:
            self.g.get_node_id(0, 3)
            self.assertEqual(True, False,
                             'get_node_id should raise exception (x>row)')
        except AssertionError:
            pass
        try:
            self.g.get_node_id(3, 0)
            self.assertEqual(True, False,
                             'get_node_id should raise exception (y>column)')
        except AssertionError:
            pass
        node_id = self.g.get_node_id(0, 0)
        expect = 0
        self.assertEqual(node_id, expect,
                         'get_node_id: return invalid value')
        node_id = self.g.get_node_id(1, 0)
        expect = 3
        self.assertEqual(node_id, expect,
                         'get_node_id: return invalid value')

    def testGetRowColumn(self):
        try:
            self.g.get_row_column(-1)
            self.assertEqual(True, False,
                             '''
                             get_row_column should raise exception (node_id<0)
                             ''')
        except AssertionError:
            pass
        node_id = self.g.get_row_column(0)
        expect = (0, 0)
        self.assertEqual(node_id, expect,
                         'get_row_column: return invalid value')
        node_id = self.g.get_row_column(1)
        expect = (0, 1)
        self.assertEqual(node_id, expect,
                         'get_row_column: return invalid value')

    def testPaintSimple(self):
        nodes = [Node(0, 0, GRASS)] * 9
        node_id = 0
        for node in nodes:
            row, column = self.g.get_row_column(node_id)
            self.g.set_node(row, column, node)
            node_id += 1
        self.g.paint()
        nodes = nx.get_node_attributes(self.g.graph, 'nodes')
        for n in nodes:
            self.assertEqual(nodes[n].is_painted(), True)

    def testPaintPerimeterCase(self):
        self.g = Graph(5, 5)
        nodes = [
                 [Node(0, 0, GRASS), 
                  Node(0, 0, GRASS),
                  Node(0, 0, GRASS),
                  Node(0, 0, GRASS),
                  Node(0, 0, GRASS)],
                 [Node(0, 0, GRASS), 
                  Node(0, 0, BLOCK),
                  Node(0, 0, BLOCK),
                  Node(0, 0, BLOCK),
                  Node(0, 0, GRASS)],
                 [Node(0, 0, GRASS), 
                  Node(0, 0, BLOCK),
                  Node(0, 0, GRASS),
                  Node(0, 0, BLOCK),
                  Node(0, 0, GRASS)],
                 [Node(0, 0, GRASS), 
                  Node(0, 0, BLOCK),
                  Node(0, 0, BLOCK),
                  Node(0, 0, BLOCK),
                  Node(0, 0, GRASS)],
                 [Node(0, 0, GRASS), 
                  Node(0, 0, GRASS),
                  Node(0, 0, GRASS),
                  Node(0, 0, GRASS),
                  Node(0, 0, GRASS)]
                ]
        for row in range(0, len(nodes)):
            for column in range(0, len(nodes[row])):
                self.g.set_node(row, column, nodes[row][column])
        self.g.paint()
        expect = [
                  True, True, True, True, True,
                  True, False, False, False, True,
                  True, False, False, False, True,
                  True, False, False, False, True,
                  True, True, True, True, True
                 ]
        nodes = nx.get_node_attributes(self.g.graph, 'nodes')
        for n in nodes:
            self.assertEqual(nodes[n].is_painted(), expect[n])

    def testDraw(self):
        nodes = [Node(0, 0, GRASS)] * 9
        node_id = 0
        for node in nodes:
            row, column = self.g.get_row_column(node_id)
            self.g.set_node(row, column, node)
            node_id += 1
        self.g.draw(self.screen)

    def testIterate(self):
        nodes = [Node(0, 0, GRASS)] * 9
        node_id = 0
        for node in nodes:
            row, column = self.g.get_row_column(node_id)
            self.g.set_node(row, column, node)
            node_id += 1
        expect = '3:x=0y=0player=0'
        count = 0
        for n in self.g.iterate():
            count += 1
            self.assertEqual(str(n),expect)
        self.assertEqual(count, 9)
        count = 0
        for n in self.g.iterate(row=0):
            count += 1
            self.assertEqual(str(n),expect)
        self.assertEqual(count, 3)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()