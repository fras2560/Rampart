'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game to store cannons, castles, walls
'''
from terrain import Terrain
import os
import unittest
from piece import Piece
from math import pi
from config import DOWN,UP,LEFT,RIGHT,EMPTY,BLOCK,CANNON,GRASS,PAINTED, WALL
from config import WATER,UP,DOWN,LEFT,RIGHT,NO_MOVE,CLOCKWISE,COUNTER_CLOCKWISE
from config import TERRAIN

'''
--------------------------------------------------------------------------------
'''

class MatrixError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Matrix():
    def __init__(self, row=None, column=None):
        
        self._matrix = []
        if row is not None and row > 0:
            if column is not None and column > 0:
                self.initialize(row, column)
                self.row = row
                self.column = column

    def initialize(self, row, column):
        '''
        a function that can will initialize the
        matrix to be row*column of zeros
        Parameters:
            row: the row dimension
            column: the column dimension
        Return
            None
        '''
        if row > 0 and column > 0:
            self._matrix = []
            self.column = column
            self.row = row
            r = 0
            while r < row:
                c = 0
                rw = []
                while c < column:
                    rw.append(EMPTY)
                    c += 1
                self._matrix.append(rw)
                r+=1
        else:
            raise Exception("Matrix not inialized properly")

    def init_paint(self, row, column):
        if row > 0 and column > 0:
            self._paint = []
            self.column = column
            self.row = row
            r = 0
            while r < row:
                c = 0
                rw = []
                while c < column:
                    rw.append(EMPTY)
                    c += 1
                self._paint.append(rw)
                r+=1
        else:
            raise Exception("Matrix not inialized properly")

    def print_m(self):
        '''
        a function to print the matrix
        Parameters:
            None
        Returns:
            None
        '''
        for r in self._matrix:
            output = ""
            for cell in r:
                output +=  str(cell) + " "
            print(output)
        print("-----------")

    def print_paint(self):
        '''
        a function to print the paint
        Parameters:
            None
        Returns:
            None
        '''
        for r in self._paint:
            output = ""
            for cell in r:
                output +=  str(cell) + " "
            print(output)
        print("-----------")

    def set_cell(self,row,column,value):
        '''
        a setter function to set an element of the matrix at position (row,column)
        Parameters:
            row: the row index of the matrix
            column: the column index of the matrix
            value: the value of matrix position
        Returns:
            None
        Raises MatrixError
            If access is outside matrix range
        '''
        if(row >= len(self._matrix)):
            raise MatrixError("Matrix row was accessed outside of range")
        if(column >=  len(self._matrix[0])):
            raise MatrixError("Matrix column was accessed outside of range")
        if(column < 0 or row < 0):
            raise MatrixError("Matrix column was accessed outside of range")
        self._matrix[row][column] = value

    def get_cell(self, row, column):
        '''
        a getter function to get an element of the matrix at position (row,column)
        Parameters:
            row: the row index of the matrix
            column: the column index of the matrix
        Returns:
            None
        Raises MatrixError
            If access is outside matrix range
        '''
        if(row >= len(self._matrix)):
            raise MatrixError("Matrix row was accessed outside of range")
        if(column >=  len(self._matrix[0])):
            raise MatrixError("Matrix column was accessed outside of range")
        if(column < 0 or row < 0):
            raise MatrixError("Matrix column was accessed outside of range")
        return self._matrix[row][column]

    def create_empty_row(self):
        '''
        a function that creates an empty row of zeros
        Parameters:
            None
        Returns:
            row: a list of zero (size n)
        '''
        row = []
        r = 0
        while r < self.row:
            row.append(EMPTY)
            r+=1
        return row

    def check_lines(self):
        '''
        a function that check and delete any completed rows
        Parameters:
            None
        Returns:
            lines: a list of the rows completed
        '''
        lines = []
        row = 0
        while row < self.row:
            complete = True
            col = 0
            while complete and col < self.column:
                if self._matrix[row][col] == EMPTY:
                    complete = False
                else:
                    col +=1 
            if complete:
                del self._matrix[row]
                self._matrix.insert(EMPTY, self.create_empty_row())
                lines.append(row)
            row += 1
        return lines

    def add_piece(self,piece):
        '''
            a function that adds the piece to the matrix
            Parameters:
                piece: a object of class piece
            Returns:
                None
        '''
        points = piece.return_points()
        valid = True
        for point in points:
            x = point[0][0]
            y = point[1][0]
            try:
                self.set_cell(y, x, BLOCK)
            except MatrixError:
                print("Should Have not a got a matrix error")
                valid = False
        return valid

    def check_valid(self,piece):
        '''
            a function that checks if the piece's position is valid in the matrix
            Parameters:
                piecE: the piece object
            Returns:
                True if piece position is valid
                False otherwise
        '''
        points = piece.return_points()
        valid = True
        for point in points:
            x = point[0][0]
            y = point[1][0]
            if x < 0 or y < 0:
                valid = False
                break;
            if x >= self.column or y >=self.row:
                valid = False
                break;
            self.get_cell(y, x)
            if(self.get_cell(y, x) != EMPTY):
                valid = False
                break;
        return valid

    def move_right(self, piece):
        '''
        a function the moves the piece to the right
        Parameters:
            piece: of class piece
        Returns:
            True of piece was moved
            False otherwise
        '''
        piece.translate(RIGHT,NO_MOVE)
        moved = True
        if not self.check_valid(piece):
            piece.translate(LEFT,NO_MOVE)
            moved = False
        return moved

    def move_left(self, piece):
        '''
        a function the moves the piece to the left
        Parameters:
            piece: of class piece
        Returns:
            True of piece was moved
            False otherwise
        '''
        piece.translate(LEFT,NO_MOVE)
        moved = True
        if not self.check_valid(piece):
            piece.translate(RIGHT,NO_MOVE)
            moved = False
        return moved

    def move_down(self,piece):
        '''
        a function that moves the piece down
        Parameters:
            piece: the piece to move down
        Returns:
            True if piece was moved
            False otherwise
        '''
        piece.translate(NO_MOVE,DOWN)
        moved = True
        if not self.check_valid(piece):
            piece.translate(NO_MOVE,UP)
            moved = False
        return moved

    def rotate_piece(self,piece):
        '''
        a function that rotates the piece if possible
        Parameters:
            piece: the piece to rotate
        Returns:
            True if piece was rotated
            False otherwise
        '''
        piece.rotate(CLOCKWISE)
        moved = True
        if not self.check_valid(piece):
            piece.rotate(COUNTER_CLOCKWISE)
            moved = False
        return moved

    def paint_matrix_aux(self,x,y):
        '''
        a recursive function that will continue to paint a matrix while avoid walls
        Parameters:
            x: the x position in the matrix
            y: the y location in the matrix
        
        '''
        #current square
        if(self._paint[x][y] != PAINTED):
            self._paint[x][y] = PAINTED
        #up left
        if(self.valid_position(x+LEFT,y+UP)):
            self.paint_matrix_aux(x+LEFT, y+UP)
        #up
        if(self.valid_position(x,y+UP)):
            self.paint_matrix_aux(x, y+UP)
        #up right
        if(self.valid_position(x+RIGHT,y+UP)):
            self.paint_matrix_aux(x+RIGHT, y+UP)
        #left
        if(self.valid_position(x+LEFT,y)):
            self.paint_matrix_aux(x+LEFT, y)
        #right
        if(self.valid_position(x+RIGHT,y)):
            self.paint_matrix_aux(x+RIGHT, y)
        #bottom left
        if(self.valid_position(x+LEFT,y+DOWN)):
            self.paint_matrix_aux(x+LEFT, y+DOWN)
        #bottom
        if(self.valid_position(x,y+DOWN)):
            self.paint_matrix_aux(x, y+DOWN)
        #bottom right
        if(self.valid_position(x+RIGHT,y+DOWN)):
            self.paint_matrix_aux(x+RIGHT, y+DOWN)

    def paint_matrix(self,x,y):
        '''
        a function to paint a matrix while avoiding walls
        Parameters:
            x: the starting x position
            y: the starting y position
        '''
        self.init_paint(self.row, self.column)
        self.paint_matrix_aux(x, y)

    def valid_position(self,x,y):
        '''
            a function that checks if the coordinates given are valid positions
            Parameters:
                x: the x position
                y: the y position
            Returns
                True if valid
                False otherwise
        '''
        return (x >= 0 and 
            x < len(self._matrix[0]) and 
            y >= 0 and y < len(self._matrix) and 
            self._paint[x][y] != PAINTED and
            self._matrix[x][y] != BLOCK)

    def load_level(self,file):
        '''
        a function to load the level from a file
        Parameters:
            file: the filename
        Returns:
            {success:Boolean, Error:Message}
        '''
        fp = os.path.join('levels',file)
        result = {}
        result['succcess'] = True
        resized = False
        skip = True
        pos = 0
        try:
            with open(fp) as f:
                row = 0
                for line in f:
                    if not skip:
                        cells = line.split(',')
                        if not resized:
                            num_lines = sum(1 for line in open(fp))
                            self.initialize(num_lines-2, len(cells))
                            resized = True
                        column = 0
                        for cell in cells:
                            self._matrix[row][column] = int(cell)
                            column += 1
                        row +=1
                    else:
                        if pos >= 1:
                            skip = False
                        pos += 1
                        
        except:
            result['error'] = "Unknown Error"
        return result

    def get_position(self,x,y):
        '''
        a function to determine what call the x,y position lies in
        Parameters:
            x: the x position of the point
            y: the y position of the point
        Returns:
            (column,row)
        '''
        return(x/TERRAIN, y/TERRAIN)

    def update_square(self,x,y,terrain):
        '''
        a function to update a specfic square
        Parameters:
            x: the x position of the square
            y: the y position of the sqaure
            terrain: the type of terrain to update to
        Returns:
            None
        '''
        row = y / TERRAIN
        column = x / TERRAIN
        self._matrix[row][column] = terrain

    def save_level(self):
        '''
        a function that saves the matrix to a txt file
        Parameters:
            None
        Returns:
            None
        '''
        fp = os.path.join('levels',"saved_level.txt")
        with open(fp, "a") as f:
            for row in self._matrix:
                r = str(row[0])
                for cell in row[1:]:
                    r += "," + str(cell)
                r += "\n"
                f.write(r)
        return

class test_case(unittest.TestCase):

    def setUp(self):
        self.m = Matrix(3,3)
        self.p = Piece()
        self.p._T_piece()

    def tearDown(self):
        pass

    def test_print_m(self):
        '''
        If it runs then it passes
        '''
        print("Print Test")
        print("----------")
        self.m.print_m()
        print("----------")

    def test_set_cell(self):
        self.m.set_cell(1, 1, 1)
        self.assertEqual(self.m._matrix[1][1],1)
        try:
            self.m.set_cell(2, 3, 1)
            self.assertEqual(False, True)
        except MatrixError:
            pass
        try:
            self.m.set_cell(3, 3, 1)
            self.assertEqual(False, True)
        except MatrixError:
            pass
        try:
            self.m.set_cell(4, 2, 1)
            self.assertEqual(False, True)
        except MatrixError:
            pass

    def test_create_empty_row(self):
        result = self.m.create_empty_row()
        self.assertEqual(result, [0,0,0])

    def test_check_lines(self):
        self.m.set_cell(0, 1, 1)
        self.m.set_cell(1, 0, 1)
        self.m.set_cell(1, 1, 1)
        self.m.set_cell(1, 2, 1)
        self.m.set_cell(2, 2, 1)
        matrix = [[0,0,0],[0,1,0],[0,0,1]]
        result = self.m.check_lines()
        self.assertEqual(result,[1])
        self.assertEqual(self.m._matrix, matrix)

    def test_add_piece(self):
        self.m = Matrix(3,3)
        self.p.translate(1,0)
        self.m.add_piece(self.p)
        expected = [[1,1,1],[0,1,0],[0,0,0]]
        self.assertEqual(expected, self.m._matrix)

    def test_check_valid(self):
        self.m.set_cell(2, 2, 1)
        self.p.translate(1,1)
        overlap = self.m.check_valid(self.p)
        self.assertEqual(overlap, True )
        self.m.initialize(3, 3)
        self.m.set_cell(1, 1, 1)
        self.p.reset()
        self.p._Z_piece()
        self.p.translate(1,1)
        overlap = self.m.check_valid(self.p)
        self.assertEqual(overlap, False)

    def test_move_right(self):
        self.m = Matrix(3,3)
        moved = self.m.move_right(self.p)
        self.assertEqual(moved,True)
        moved = self.m.move_right(self.p)
        self.assertEqual(moved,False)

    def test_move_left(self):
        self.m = Matrix(3,3)
        moved = self.m.move_left(self.p)
        self.assertEqual(moved,False)
        moved = self.m.move_right(self.p)
        self.assertEqual(moved,True)
        moved = self.m.move_left(self.p)
        self.assertEqual(moved,False)
        self.p.translate(1,0)
        moved = self.m.move_left(self.p)
        self.assertEqual(moved,True)

    def test_move_down(self):
        moved = self.m.move_right(self.p)#moved into play
        self.assertEqual(moved, True)
        moved = self.m.move_down(self.p)
        self.assertEqual(moved, True)
        self.m.set_cell(2, 1, 1)
        self.p.translate(0,-1)
        moved = self.m.move_down(self.p)
        self.assertEqual(moved, False)

    def test_rotate_piece(self):
        self.m.initialize(4, 4)
        moved = self.m.move_right(self.p)#moved into play
        self.assertEqual(moved, True)
        moved = self.m.move_right(self.p)#moved into play
        self.assertEqual(moved, True)
        moved = self.m.move_down(self.p)#moved into play
        self.assertEqual(moved, True)
        self.m.add_piece(self.p)
        self.m.initialize(4, 4)
        #90 rotation
        rotate = self.m.rotate_piece(self.p)
        self.assertEqual(rotate, True)
        self.m.add_piece(self.p)
        expected = [[0,0,1,0],[0,0,1,1],[0,0,1,0],[0,0,0,0]]
        self.assertEqual(expected, self.m._matrix)
        #180 rotation
        self.m.initialize(4, 4)
        rotate = self.m.rotate_piece(self.p)
        self.assertEqual(rotate, True)
        self.m.add_piece(self.p)
        expected = [[0,0,1,0],[0,1,1,1],[0,0,0,0],[0,0,0,0]]
        self.assertEqual(expected, self.m._matrix)
        #270 rotation
        self.m.initialize(4, 4)
        rotate = self.m.rotate_piece(self.p)
        self.assertEqual(rotate, True)
        self.m.add_piece(self.p)
        expected = [[0,0,1,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]]
        self.assertEqual(expected, self.m._matrix)
        #one full rotation
        self.m.initialize(4, 4)
        rotate = self.m.rotate_piece(self.p)
        self.assertEqual(rotate, True)
        self.m.add_piece(self.p)
        expected = [[0,0,0,0],[0,1,1,1],[0,0,1,0],[0,0,0,0]]
        self.assertEqual(expected, self.m._matrix)

    def test_valid_position(self):
        self.m.init_paint(self.m.row, self.m.column)
        #invalid options
        invalid = self.m.valid_position(3, 3)
        self.assertEqual(invalid,False)
        invalid = self.m.valid_position(-1, 2)
        self.assertEqual(invalid,False)
        invalid = self.m.valid_position(-4, 4)
        self.assertEqual(invalid,False)
        invalid = self.m.valid_position(0, -2)
        self.assertEqual(invalid,False)
        invalid = self.m.valid_position(0, 3)
        self.assertEqual(invalid,False)
        #valid options
        valid = self.m.valid_position(0, 0)
        self.assertEqual(valid,True)
        valid = self.m.valid_position(2, 0)
        self.assertEqual(valid,True)
        valid = self.m.valid_position(0, 2)
        self.assertEqual(valid,True)
        valid = self.m.valid_position(2, 2)
        self.assertEqual(valid,True)
        
        # a BLOCK
        self.m.set_cell(0,0,BLOCK)
        valid = self.m.valid_position(0, 0)
        self.assertEqual(valid,False)
        
        #already PAINTED
        self.m._paint[1][1] = PAINTED
        valid = self.m.valid_position(1, 1)
        self.assertEqual(valid,False)

    def test_paint_matrix(self):
        #complete square
        self.m.initialize(5, 5)
        self.m.set_cell(1, 1, BLOCK)
        self.m.set_cell(2, 1, BLOCK)
        self.m.set_cell(3, 1, BLOCK)
        self.m.set_cell(1, 2, BLOCK)
        self.m.set_cell(3, 2, BLOCK)
        self.m.set_cell(1, 3, BLOCK)
        self.m.set_cell(2, 3, BLOCK)
        self.m.set_cell(3, 3, BLOCK)
        self.m.paint_matrix(0,0)
        expected = [[PAINTED,PAINTED,PAINTED,PAINTED,PAINTED],
                    [PAINTED,0,0,0,PAINTED],
                    [PAINTED,0,0,0,PAINTED],
                    [PAINTED,0,0,0,PAINTED],
                    [PAINTED,PAINTED,PAINTED,PAINTED,PAINTED]]
        self.assertEqual(self.m._paint,expected)
        self.m.paint_matrix(2,2)
        expected = [[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,PAINTED,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
        self.assertEqual(self.m._paint,expected)

    def test_paint_matrix_2(self):
        #cracked square
        self.m.initialize(5, 5)
        self.m.set_cell(2, 1, BLOCK)
        self.m.set_cell(3, 1, BLOCK)
        self.m.set_cell(1, 2, BLOCK)
        self.m.set_cell(3, 2, BLOCK)
        self.m.set_cell(1, 3, BLOCK)
        self.m.set_cell(2, 3, BLOCK)
        self.m.set_cell(3, 3, BLOCK)
        self.m.paint_matrix(0,0)
        expected = [[PAINTED,PAINTED,PAINTED,PAINTED,PAINTED],
                    [PAINTED,PAINTED,0,0,PAINTED],
                    [PAINTED,0,PAINTED,0,PAINTED],
                    [PAINTED,0,0,0,PAINTED],
                    [PAINTED,PAINTED,PAINTED,PAINTED,PAINTED]]
        self.assertEqual(self.m._paint,expected)
        self.m.paint_matrix(2,2)
        expected = [[PAINTED,PAINTED,PAINTED,PAINTED,PAINTED],
                    [PAINTED,PAINTED,0,0,PAINTED],
                    [PAINTED,0,PAINTED,0,PAINTED],
                    [PAINTED,0,0,0,PAINTED],
                    [PAINTED,PAINTED,PAINTED,PAINTED,PAINTED]]
        self.assertEqual(self.m._paint,expected)

    def test_paint_matrix_3(self):
        #house with leaky roof
        self.m.initialize(7, 7)
        #roof
        self.m.set_cell(1, 3, BLOCK)
        self.m.set_cell(2, 2, BLOCK)
        self.m.set_cell(2, 4, BLOCK)
        #side
        self.m.set_cell(3, 1, BLOCK)
        self.m.set_cell(4, 1, BLOCK)
        self.m.set_cell(5, 1, BLOCK)
        self.m.set_cell(3, 5, BLOCK)
        self.m.set_cell(4, 5, BLOCK)
        self.m.set_cell(5, 5, BLOCK)
        #base
        self.m.set_cell(5, 1, BLOCK)
        self.m.set_cell(5, 2, BLOCK)
        self.m.set_cell(5, 3, BLOCK)
        self.m.set_cell(5, 4, BLOCK)
        self.m.set_cell(5, 5, BLOCK)
       
        self.m.set_cell(0, 0, BLOCK)
        self.m.paint_matrix(0,0)
        expected = [[PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED],
                    [PAINTED, PAINTED, PAINTED, 0, PAINTED, PAINTED, PAINTED],
                    [PAINTED, PAINTED, 0, PAINTED, 0, PAINTED, PAINTED],
                    [PAINTED, 0, PAINTED, PAINTED, PAINTED, 0, PAINTED],
                    [PAINTED, 0, PAINTED, PAINTED, PAINTED, 0, PAINTED],
                    [PAINTED, 0, 0, 0, 0, 0, PAINTED],
                    [PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED],]
        self.assertEqual(self.m._paint,expected)

    def test_paint_matrix_4(self):
        #house with reinforced roof
        self.m.initialize(7, 7)
        #roof
        self.m.set_cell(1, 3, BLOCK)
        self.m.set_cell(2, 2, BLOCK)
        self.m.set_cell(2, 3, BLOCK)      
        self.m.set_cell(2, 4, BLOCK)
        self.m.set_cell(3, 2, BLOCK)
        self.m.set_cell(3, 4, BLOCK)
        
        #side
        self.m.set_cell(3, 1, BLOCK)
        self.m.set_cell(4, 1, BLOCK)
        self.m.set_cell(5, 1, BLOCK)
        self.m.set_cell(3, 5, BLOCK)
        self.m.set_cell(4, 5, BLOCK)
        self.m.set_cell(5, 5, BLOCK)
        #base
        self.m.set_cell(5, 1, BLOCK)
        self.m.set_cell(5, 2, BLOCK)
        self.m.set_cell(5, 3, BLOCK)
        self.m.set_cell(5, 4, BLOCK)
        self.m.set_cell(5, 5, BLOCK)
       
        self.m.set_cell(0, 0, BLOCK)
        self.m.paint_matrix(0,0)
        expected = [[PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED], 
                    [PAINTED, PAINTED, PAINTED, 0, PAINTED, PAINTED, PAINTED],
                    [PAINTED, PAINTED, 0, 0, 0, PAINTED, PAINTED ],
                    [PAINTED, 0, 0, 0, 0, 0, PAINTED ],
                    [PAINTED, 0, 0, 0, 0, 0, PAINTED ],
                    [PAINTED, 0, 0, 0, 0, 0, PAINTED ],
                    [PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED, PAINTED ],]
        self.assertEqual(self.m._paint,expected)

    def test_load_level(self):
        self.m.load_level("test.txt")
        first = 50*[5]
        rest = [WALL,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,
                GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,
                GRASS,WATER,WATER,WATER,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,
                GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,
                GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,WALL]
        self.assertEqual(first, self.m._matrix[0])
        for x in range(1, len(self.m._matrix)-1):
            self.assertEqual(rest, self.m._matrix[x])

    def test_update_square(self):
        terrain = WALL
        x = 15
        y = 15
        before  = self.m._matrix[1][1]
        self.m.update_square(x, y, terrain)
        result = self.m._matrix[1][1]
        self.assertNotEqual(before, result)
        self.assertEqual(result, WALL)
    
    def test_save_file(self):
        self.m.save_level()
        path = os.path.join('levels',"saved_level.txt")
        self.assertEqual(os.path.isfile(path), True)
        with open(path) as f:
            for line in f:
                self.assertEqual("0,0,0\n", line)
        os.remove(path)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()      
