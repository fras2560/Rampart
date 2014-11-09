'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import math
import unittest
from rampart.explosion import Explosion
from rampart.point import Point
from rampart.color import Color
from rampart.config import ARC
import pygame

class Bezier():
    def __init__(self):
        self.points = []
        self.coeffs = []

    def reset(self):
        '''
        a method to reset the bezier curve
        Parameters:
            None
        Returns:
            None
        '''
        del self.points
        del self.coeffs
        self.points = []
        self.coeffs = []

    def add_point(self,point):
        '''
        a method to add a control point
        Parameters:
            point: the point to add (Point)
        Returns:
            None
        '''
        self.points.append(point)

    def set_coeffs(self):
        '''
        a method that set the coefficients for the blending function
        Parameters:
            None
        Returns:
            None
        '''
        n = len(self.points) - 1
        self.coeffs = []
        for k in range(n + 1):
            self.coeffs.append(1)
            j = n
            while j >= k + 1:
                self.coeffs[k] *= j
                j -= 1
            j= n - k
            while j >= 2:
                self.coeffs[k] /=j
                j -= 1

    def get_point(self, u):
        '''
        a method that calculate the bezier point
        Parameters:
            u: the value of u for blending function (p1=0<=u<=1.0=pn) (float)
        Returns:
            point: an object with the x and  position (Point)
        '''
        control_points = len(self.points)
        n = control_points - 1
        point = Point()
        point.set(x=0, y=0)
        k = 0
        while k < control_points:
            blend_function = self.coeffs[k] * math.pow(u, k) * math.pow(1-u,
                                                                        n-k)
            (x, y) = self.points[k].get()
            (xi, yi) = point.get()
            point.set(x=xi + x * blend_function, y=yi + y * blend_function)
            k += 1
        return point 

class TestBezier(unittest.TestCase):
    def setUp(self):
        self.b = Bezier()
        
    def tearDown(self):
        pass

    def test_add_point(self):
        self.assertEqual(self.b.points, [])
        p = Point()
        p.set(x=1,y=1)
        self.b.add_point(p)
        self.assertEqual([p], self.b.points)

    def test_set_coeffs(self):
        p1 = Point().set(x=1, y=1)
        p2 = Point().set(x=2, y=2)
        p3 = Point().set(x=3, y=1)
        self.b.points = [p1, p2, p3]
        self.b.set_coeffs()
        self.assertEqual(self.b.coeffs,[1, 2, 1])

    def test_get_point(self):
        p1 = Point()
        p1.set(x=1, y=1)
        p2 = Point()
        p2.set(x=2, y=2)
        p3 = Point()
        p3.set(x=3, y=1)
        self.b.coeffs = [1, 3, 1]
        self.b.points = [p1,p2,p3]
        u = 0
        x = 0
        n = len(self.b.points)
        p = Point()
        p.set(x=0, y=0)
        while x <= n:
            u = x / float(n)
            p = self.b.get_point(u)
            x += 1

class Equation():
    def __init__(self):
        '''
        velocity: the initial velocity
        y0: the y0 coordinate
        time: the current time of the equation
        step: how much time to move per iteration
        x0: the x0 coordinate
        vertical: True if movement is only vertical False otherwise
        g: the gravity constant
        '''
        self.bezier = Bezier()
        self.u = 0
        self.step = 0
        self.tol = 10
        self.done = False
        self.velocity = 10

    def reset(self):
        '''
        a method to reset the equation
        Parameters:
            None
        Returns:
            None
        '''
        self.bezier.reset()
        self.u = 0
        self.step = 0
        self.tol = 10
        self.done = False
        self.velocity = 1
        
    def set(self,p1, p2):
        '''
        a method that set the equation using the two points given
        Parameters:
            p1: the first point or initial release point (Point)
            p2: the second point or target point (Point)
        Returns:
            None
        '''
        (x1,y1) = p1.get()
        (x2,y2) = p2.get()
        right = x2 - x1 > 0
        up = y2 - y1 > 0
        dx = math.fabs(x1 - x2)
        dy = math.fabs(y1 - y2)
        euclidean = math.sqrt(dx * dx + dy * dy)
        distance = min(euclidean, ARC)
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        mid_y = my # assume in the middle
        mid_x = mx # assume in the middle
        if (dx < self.tol and dx < dy / 2):
            mid_x = max(x1, x2) + distance
        elif (dy < self.tol  and dy < dx / 2):
            mid_y = min(y1, y2) - distance
        else:
            if right and up:
                mid_y += distance
                mid_x -= distance
            elif right and not up:
                mid_y -= distance
                mid_x += distance
            elif not right and up:
                mid_y -= distance
                mid_x += distance
            elif not right and not up:
                mid_y -= distance
                mid_x -= distance
        print(distance, mid_x, mid_y)
        #set the the step size
        self.step = 1 / float(euclidean) * self.velocity
        # add the three points
        self.bezier.add_point(p1)
        pmid = Point()
        pmid.set(mid_x, mid_y)
        self.bezier.add_point(pmid)
        self.bezier.add_point(p2)
        self.bezier.set_coeffs()
        return 

    def get(self):
        '''
        a method that gets the current position of the equation
        Parameters:
            None:
        Returns:
            point: the current point (Point)
        '''
        p = self.bezier.get_point(self.u)
        self.u += self.step
        if(self.u >= 1.0):
            self.done = True
        return p

'''
Currently no test for equation since it depends on GRAVITY constant
will write tests once decide on gravity constant
'''

class Cannonball(pygame.sprite.Sprite):
    def __init__(self):
        '''
        equation: the equation of the cannon ball path
        _shoot: a boolean telling whether the cannon ball
                      has been shot
        end: the ending point of the cannonball
        position: the curremt position of the cannonball
        color: a color class
        image: the image of the cannonball
        rect: the image position of the image
        bomb: the explosion object
        exploding: a variable telling if the cannonball is exploding or not
        '''
        pygame.sprite.Sprite.__init__(self)
        self.equation = Equation()
        self._shoot = False
        self.end = None
        self.position = None
        self.color = Color()
        self.bomb = Explosion()
        self.exploding = False

    def reset(self):
        '''
        a method that resets the Cannonball
        Parameters:
            None
        Returns:
            None
        '''
        self.equation.reset()
        self._shoot = False
        self.end = None
        self.position = None
        self.x = -1
        self.y = -1
        self.exploding = False

    def set(self, p1, p2):
        '''
        a method that two sets of points for the cannon ball path
        Parameters:
            p1: a tuple of the point (x,y)
            p2: a tuple of the second point (x2,y2)
        Returns:
            None
        '''
        self.equation.set(p1,p2)
        self.end = p2
        self._shoot = True
        self.exploding = False
        self.position = p1
        (x,y) = p1.get()
        self.x = x
        self.y = y
        
    def in_air(self):
        '''
        a method that checks if the cannon ball is  in the air or not
        Parameters:
            None
        Returns:
            True if still in air False otherwise
        '''
        return self._shoot

    def increment(self):
        '''
        a method that moves the position of the cannonball
        and determines if the cannonball has reached the end position
        Parameters:
            None
        Returns
            None
        '''
        self.position = self.equation.get()
        if self.equation.done:
            self.exploding = True
            self.bomb.set(self.end)
        return

    def past_end(self, a, b, direction):
        '''
        a method that checks if the a (point) is past the b point
        Parameters:
            a: the x coordinate of point
            b: the x coordinate of the second point
            direction: an int representing which direction the point is moving
        Returns:
            True if past
            False otherwise
        '''
        past = False
        if a > b and direction > 0:
            past = True
        elif a < b and direction < 0:
            past = True
        elif a == b:
            past = True
        return past
    
    def get(self):
        '''
        a method that gets position of the cannonball
        Parameters:
            None
        Returns:
            (x1,y1): a tuple fo the x and y position
        '''
        return self.position.get()
    
    def update(self):
        '''
        the method to update the cannonball position
        Parameters:
            none
        Returns:
            None
        '''
        if self._shoot and not self.exploding:
            self.increment()
            (x,y) = self.position.get()
            self.x = x
            self.y = y
    
    def draw(self, surface):
        '''
        a method to draw the cannonball or explosion
        Parameters:
            surface: the surface to draw on
        Returns:
            None
        '''
        point = (int(self.x), int(self.y))
        if not self.exploding:
            pygame.draw.circle(surface, self.color.black,
                               point, 5, 0)
            pygame.draw.circle(surface, self.color.red,
                               point, 2, 0)
        else:
            self.bomb.update()
            self.bomb.draw(surface)
            if self.bomb.finished:
                self._shoot = False

class testCannonball(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((500,500))
        self.ball = Cannonball()
        self.start = Point()
        self.start.set(x=100,y=100)
        self.end = Point()
        self.end.set(x=150,y=150)

    def tearDown(self):
        self.ball.reset()
        pygame.quit()

    def test_set(self):
        self.ball.set(self.start,self.end)
        self.assertEqual(self.ball.exploding, False)
        self.assertEqual(self.ball._shoot, True)
        self.assertEqual(self.ball.end,self.end)
        self.assertEqual(self.ball.position,self.start)
        (x,y) = self.start.get()
        self.assertEqual(self.ball.x, x)
        self.assertEqual(self.ball.y, y)

    def test_in_air(self):
        self.assertEqual(self.ball.in_air(), False)
        self.ball._shoot = True
        self.assertEqual(self.ball.in_air(), True)

    def test_past_end(self):
        result = self.ball.past_end(1, 2, 1)
        self.assertEqual(result,False)
        result = self.ball.past_end(1, 2, -1)
        self.assertEqual(result,True)
        result = self.ball.past_end(2, 1, -1)
        self.assertEqual(result,False)
        result = self.ball.past_end(3, 2, 1)
        self.assertEqual(result,True)
        result = self.ball.past_end(2, 2, 1)
        self.assertEqual(result,True)
        result = self.ball.past_end(2, 2, -1)
        self.assertEqual(result,True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()