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
import networkx as nx
from rampart.config import PAINTED, BLOCK

class Graph():
    def __init__(self, row, column):
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

    def get_node_id(self, row, column):
        '''
        a method the finds the node id for the (x,y) pair given
        Parameters:
            row: the row in which the node is located (int >= 0)
            column: the column in which the node is located (int >= 0)
        '''
        assert row >= 0, 'Graph->get_node_id: invalid row index (<0)'
        assert column >= 0, 'Graph->get_node_id: invalid column index (<0)'
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
            node.draw()

    def paint(self):
        '''
        a method use to paint the nodes starting a top left and moving 
        to each nodes neighbors unless blocked by a block
        '''
        # reset to not painted
        nodes = nx.get_node_attributes(self.graph, 'nodes')
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
            for neighbor in self.graphs.neighbors(node_id):
                self.paint_aux(neighbor)
        return

import unittest

class Test(unittest.TestCase):

    def setUp(self):
        self.rows = 3
        self.columns = 3
        self.g = Graph(self.rows, self.columns)

    def tearDown(self):
        pass

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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()