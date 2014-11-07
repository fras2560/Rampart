'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import unittest
from random import randint
from math import cos,sin,pi
from rampart.config import NODE_SIZE
import pprint
import pygame

class PieceError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Piece():
    '''
    a Piece which holds blocks to add to the level
    '''
    def __init__(self):
        '''
        Parameters:
            None
        Properties:
            points: the block points
            rotation_matrix: the matrix which holds the rotations
            translation_matrix: the matrix which holds translations
        '''
        self.points = []
        self.rotation_matrix = [[1,0],[0,1]] #elementary matrix
        self.translation_matrix = [[0,0],[0,0]]

    def reset(self):
        '''
        a method that resets the Piece position
        Parameters:
            None
        Returns:
            None
        '''
        self.points = []
        self.rotation_matrix = [[1,0],[0,1]] #elementary matrix
        self.translation_matrix = [[0,0],[0,0]]

    def _I_piece(self):
        '''
        a method to create an I piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append([[0],[-NODE_SIZE]])
        self.points.append([[0],[NODE_SIZE]])
        self.points.append([[0],[2 * NODE_SIZE]])
        self.points.append([[0],[0]])
    
    def _J_piece(self):
        '''
        a method to create an J piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append( [[0],[0]])
        self.points.append( [[0],[NODE_SIZE]])
        self.points.append( [[0],[-NODE_SIZE]])
        self.points.append( [[NODE_SIZE],[NODE_SIZE]])

    def _L_piece(self):
        '''
        a method to create an L piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append( [[0],[0]])
        self.points.append( [[0],[NODE_SIZE]])
        self.points.append( [[0],[-NODE_SIZE]])
        self.points.append( [[-NODE_SIZE],[NODE_SIZE]])

    def _O_piece(self):
        '''
        a method to create an O piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append( [[0],[0]])
        self.points.append( [[0],[NODE_SIZE]])
        self.points.append( [[NODE_SIZE],[0]])
        self.points.append( [[NODE_SIZE],[NODE_SIZE]])

    def _T_piece(self):
        '''
        a method to create an T piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append( [[0],[0]])
        self.points.append( [[NODE_SIZE],[0]])
        self.points.append( [[-NODE_SIZE],[0]])
        self.points.append( [[0],[NODE_SIZE]])

    def _Z_piece(self):
        '''
        a method to create an Z piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append([[0],[0]])
        self.points.append([[0],[-NODE_SIZE]])
        self.points.append([[NODE_SIZE],[-NODE_SIZE]])
        self.points.append([[-NODE_SIZE],[0]])

    def _S_piece(self):
        '''
        a method to create an S piece
        Parameters:
            None
        Returns:
            None
        '''
        self.points.append( [[0],[0]])
        self.points.append([[0],[-NODE_SIZE]])
        self.points.append( [[-NODE_SIZE],[-NODE_SIZE]])
        self.points.append([[NODE_SIZE],[0]])

    def create_piece(self):
        '''
        a method used to create a random piece
        Parameters:
            None
        Returns:
            None
        '''
        piece = randint(1,7)
        self.reset()
        if piece == 1:
            self._I_piece()
        elif piece == 2:
            self._J_piece()
        elif piece == 3:
            self._L_piece()
        elif piece == 4:
            self._O_piece()
        elif piece == 5:
            self._S_piece()
        elif piece == 6:
            self._T_piece()
        elif piece == 7:
            self._Z_piece()

    def rotate(self, angle):
        '''
        a method used to rotate a piece
        Parameters:
            angle: the angle by which to rotate by (float)
        Returns:
            None
        '''
        a1 = (cos(angle)*self.rotation_matrix[0][0]
            +-sin(angle)*self.rotation_matrix[1][0])
        a2 = (cos(angle)*self.rotation_matrix[0][1]
            +-sin(angle)*self.rotation_matrix[1][1])
        a3 = (sin(angle)*self.rotation_matrix[0][0]
            +cos(angle)*self.rotation_matrix[1][0])
        a4 = (sin(angle)*self.rotation_matrix[0][1]
            +cos(angle)*self.rotation_matrix[1][1])
        self.rotation_matrix = [[int(round(a1,0)),int(round(a2,0))],
                               [int(round(a3,0)),int(round(a4,0))]]
        return

    def clockwise_turn(self):
        '''
        a method to rotate the piece clockwise by 90 degrees
        Parameters:
            None
        Returns:
            None
        '''
        self.rotate(pi/2)

    def counter_clockwise_turn(self):
        '''
        a method to rotate the piece counter-clockwise by 90 degrees
        Parameters:
            None
        Returns:
            None
        '''
        self.rotate(-pi/2)

    def translate(self, x, y):
        '''
        a method to translate a piece (x,y) over
        Parameters:
            x: the x translation (float)
            y: the y translation (float)
        Returns:
            None
        '''
        self.translation_matrix[0][0] += x
        self.translation_matrix[1][1] += y
        return

    def return_points(self):
        '''
        a method that returns the points positions
        Parameters:
            None
        Returns:
            result: the list of the points (list)
        '''
        result = []
        for point in self.points:
            p = self.matrix_multiply(self.rotation_matrix,point)
            p[0][0] += self.translation_matrix[0][0]
            p[1][0] += self.translation_matrix[1][1]
            result.append((p[0][0], p[1][0]))
        return result

    def matrix_multiply(self, m1, m2):
        '''
        a method that mutlplies the two matrices
        Parameter:
            m1: the first matrix (matrix)
            m2: the second matrix (matrix)
        Returns:
            result: the result matrix (matrix)
        '''
        row = 0
        result = []
        while row < len(m1):
            column = 0
            row_result = []
            while column < len(m2[row]):
                sum = 0
                inside = 0
                while inside < len(m1[row]):
                    sum += m1[row][inside] * m2[inside][column]
                    inside += 1
                row_result.append(sum)
                column += 1
            result.append(row_result)
            row += 1
        return result

    def draw(self, surface, color):
        '''
        a method to draw the piece outline
        Parameters:
            surface: the pygame display screen (surface)
        Returns:
            None
        '''
        points = self.return_points()
        for point in points:
            pygame.draw.rect(surface, color,
                             (point[0], point[1], NODE_SIZE, NODE_SIZE))

class test_Suite(unittest.TestCase):
    def setUp(self):
        self.p = Piece()
        self.pp = pprint.PrettyPrinter(indent=4)

    def tearDown(self):
        pass

    def test_rotate(self):
        self.p.rotate(pi/2)
        self.assertEqual(self.p.rotation_matrix, [[0.0, -1.0], [1.0, 0.0]])
        self.p.rotate(pi/2)
        self.assertEqual(self.p.rotation_matrix, [[-1.0, -0.0], [0.0, -1.0]])
        self.p.rotate(pi/2)
        self.assertEqual(self.p.rotation_matrix, [[-0.0, 1.0], [-1.0, -0.0]])
        self.p.rotate(pi/2)
        self.assertEqual(self.p.rotation_matrix, [[1.0, 0.0], [0.0, 1.0]])

    def test_transformation(self):
        self.p.translate(1, 1)
        expected = [[1,0],[0,1]]
        self.assertEqual(expected, self.p.translation_matrix)
        self.p.translate(0,1)
        expected = [[1,0],[0,2]]
        self.assertEqual(expected, self.p.translation_matrix)
    
    def test_matrix_multiply(self):
        result = self.p.matrix_multiply([[1, 0],[0, 1]],
                               self.p.rotation_matrix)
        expected = [[1,0],[0,1]]
        self.p.rotate(pi/2)
        self.assertEqual(result, expected)
        result = self.p.matrix_multiply([[1, 0],[0, 1]],
                               self.p.rotation_matrix)
        expected = [[0.0,-1],[1,0]]
        self.assertEqual(result, expected)
        self.p.translate(2, 0)
        result = self.p.matrix_multiply([[1, 0],[0, 1]],
                               self.p.rotation_matrix)
        expected = [[0.0,-1],[1,0]]

    def test_return_points(self):
        self.p._T_piece()
        self.p.rotate(-pi/2)
        result = self.p.return_points()
        expected = [(0, 0), (0, -NODE_SIZE), (0, NODE_SIZE), (NODE_SIZE, 0)]
        self.assertEqual(result, expected)
        self.p.translate(2*NODE_SIZE, 0)
        result = self.p.return_points()
        expected = [(2*NODE_SIZE, 0), (2*NODE_SIZE, -NODE_SIZE),
                    (2*NODE_SIZE, NODE_SIZE), (3*NODE_SIZE, 0)]
        self.assertEqual(result, expected)
        self.p.rotate(-pi/2)
        result = self.p.return_points()
        expected = [(2*NODE_SIZE, 0), (NODE_SIZE, 0),
                    (3*NODE_SIZE, 0), (2*NODE_SIZE, -NODE_SIZE)]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()