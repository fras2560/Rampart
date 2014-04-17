'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
from cannonball import Cannonball
from point import Point

class Canon():
    def __init__(self):
        self.ball = Cannonball()
        self.position = Point()
    
    def set(p0):
        '''
        a function that sets the position of the cannon
        '''
        self.position = p0
    
    def get(self):
        '''
        a function that sets the position of the cannon
        Parameters:
            None
        Returns:
            (x1,y1): the x and y position
        '''
    
    def draw(self):
        '''
        a function to draw the cannon
        Parameters:
            None
        Returns:
            None
        '''