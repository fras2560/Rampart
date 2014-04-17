'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import unittest

class Point():
    def __init__(self):
        self.x = None
        self.y = None

    def set(self,x=None,y=None):
        '''
        a function that sets the point values
        Parameters:
            x: the x co-ordinate of the point
            y: the y co-ordinate of the point
        Returns:
            None
        '''
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        return
    
    def get(self):
        '''
        a function that gets the points co-ordinates
        Parameters:
            None
        Returns:
            (x,y) tuple
        '''
        return (self.x,self.y)

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.p = Point()
    
    def tearDown(self):
        pass
    
    def test_get(self):
        (x,y) = self.p.get()
        self.assertEqual(x,None)
        self.assertEqual(y,None)
        self.p.x = 1
        self.p.y = 2
        (x,y) = self.p.get()
        self.assertEqual(x,1)
        self.assertEqual(y,2)
        
        
    def test_set(self):
        self.p.set(x=1)
        (x,y) = self.p.get()
        self.assertEqual(x,1)
        self.assertEqual(y,None)
        self.p.set(y=2)
        (x,y) = self.p.get()
        self.assertEqual(x,1)
        self.assertEqual(y,2)
        self.p.set(x=2,y=1)
        (x,y) = self.p.get()
        self.assertEqual(x,2)
        self.assertEqual(y,1)
