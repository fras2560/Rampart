'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import math
import unittest
from point import Point

GRAVITY = 9.81
BLACK    = (   0,   0,   0)

class Equation():
    def __init__(self):
        '''
        velocity: the initial velocity
        y0: the y0 coordinate
        time: the current time of the equation
        step: how much time to move per iteration
        x0: the x0 coordinate
        vertical: True if movement is only vertical False otherwise
        '''
        self.velocity = 0
        self.y0 = 0
        self.time = 0
        self.step = 0
        self.x0 = 0
        self.vertical = False
        self.g = 9.81

    def reset(self):
        '''
        a function to reset the equation
        Parameters:
            None
        Returns:
            None
        '''
        self.velocity = 0
        self.y0 = 0
        self.time = 0
        self.step = 0
        self.x0 = 0
        self.vertical = False
        self.g = 9.81
        
    def set_equation(self,p1,p2):
        '''
        a function that set the equation using the two points given
        Parameters:
            p1: the first point or initial release point (Point)
            p2: the second point or target point (Point)
        Returns:
            None
        '''
        (x1,y1) = p1.get()
        (x2,y2) = p2.get()
        self.y0 = y1
        self.x0 = x1
        top = float(y2) + 0.5*self.g * float(x2)*float(x2) - float(self.y0)
        self.velocity = top / float(x2)
        dx = x2 - x1
        dy = y2 - y1
        euclidean = math.sqrt(dx*dx + dy*dy)
        self.vertical  = False
        self.time = 0
        if dx < 0:
            #moving left
            self.step = -(1/euclidean)
        elif dx > 0:
            #moving right
            self.step = (1/euclidean)
        else:
            #just up/down
            self.step = (1/euclidean)
            self.vertical = True
        return

    def get_position(self):
        '''
            a function that gets the current position of the equation
            Parameters:
                None:
            Returns:
                point: the current point (Point)
        '''
        height = (-0.5*self.g*self.time*self.time + self.velocity*self.time + 
                  float(self.y0)) 
        point = Point()
        if not self.vertical:
            point.set(x=self.time+self.x0,y=height)
        else:
            point.set(x=self.x0,y=height)
        self.time += self.step
        return point

class TestEquation(unittest.TestCase):
    def setUp(self):
        self.e = Equation_2()
    
    def tearDown(self):
        pass
    
    def test_set_equation(self):
        p1 = Point()
        p1.set(x=0, y=30)
        p2 = Point()
        p2.set(x=4,y=0)
        self.e.set_equation(p1, p2)
        self.assertAlmostEqual(self.e.velocity, 12.12, 2)
        self.assertEqual(self.e.vertical, False)
        self.assertAlmostEqual(0.0330409300228, self.e.step,2)
        self.assertEqual(self.e.time,0)

    def test_get_position(self):
        self.e.velocity = 12.12
        self.e.vertical = False
        self.e.step = 0.0330409300228
        self.e.time = 0
        self.e.x0 = 0
        self.e.y0 = 30
        pos = self.e.get_position()
        (x1,y1) = pos.get()
        self.assertEqual(x1,0)
        self.assertEqual(y1,30)
        self.assertAlmostEqual(self.e.step, 0.0330409300228,2)

class Cannonball():
    def __init__(self):
        '''
        self.equation -> the equation of the cannon ball path
        self.shoot -> a boolean telling whether the cannon ball
                      has been shot
        '''
        self.equation = Equation()
        self._shoot = False
        self.end = None
        self.position = None
        self.radius = 5
    
    def reset(self):
        '''
        a function that resets the Cannonball
        Parameters:
            None
        Returns:
            None
        '''
        self.equation.reset()
        self._shoot = False
        self.end = None
        self.position = None
        self.radius = 5
        
    def set_equation(self,p1, p2):
        '''
            a function that two sets of points for the cannon ball path
            Parameters:
                p1: a tuple of the point (x,y)
                p2: a tuple of the second point (x2,y2)
            Returns:
                None
                        
        '''
        self.equation.set(p1,p2)
        self.end = p2
        self._shoot = True
        self.position = p1
        
    def in_air(self):
        '''
        a function that checks if the cannon ball is  in the air or not
        Parameters:
            None
        Returns:
            True if still in air False otherwise
        '''
        return self._shoot

    def increment(self):
        '''
        a function that moves the position of the cannonball
        and determines if the cannonball has reached the end position
        Parameters:
            None
        Returns
            None
        '''
        self.position = self.equation.get_position()
        (x1,y1) = self.position.get()
        (x2,y2) = self.end.get()
        dx = x2 - x1
        dy = y2 - y1
        euclidean = math.sqrt(dx*dx + dy*dy)
        if eucliean < self.tol:
            self.shoot = False
        return


    def get_position(self):
        '''
        a function that gets position of the cannonball
        Parameters:
            None
        Returns:
            (x1,y1): a tuple fo the x and y position
        '''
        return self.position.get()
    
    def draw(self,pygame,screen):
        '''
        the function to draw the cannon
        Parameters:
            pygame: the pygame object
            screen: the screen to draw to
        Returns:
            None
        '''
        (x,y) = self.position.get()
        pygame.draw.circle(screen, BLACK,(int(x), int(y)),int(self.radius))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()