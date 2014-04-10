'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import math
import unittest
GRAVITY = -9.8

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
        
class Bezier():
    def __init__(self):
        self.points = []
        self.coeffs = []

    def add_point(self,point):
        self.points.append(point)

    def set_coeffs(self):
        n = len(self.points) - 1
        self.coeffs = []
        for k in range(n+1):
            self.coeffs.append(1)
            j = n
            while j >=k+1:
                self.coeffs[k] *= j
                j -= 1
            j= n - k
            while j >= 2:
                self.coeffs[k] /=j
                j -= 1

    def get_point(self,u,i,point):
        
        
        control_points = len(self.points)
        n = control_points - 1
        point = Point()
        point.set(x=0,y=0)
        k = 0
        while k < control_points:
            blend_function = self.coeffs[k] * math.pow(u, k) * math.pow(1-u,n-k)
            (x,y) = self.points[k].get()
            (xi,yi) = point.get()
            point.set(x=xi+x*blend_function, y=yi+y*blend_function)
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
        p2 = Point().set(x=2,y=2)
        p3 = Point().set(x=3, y=1)
        self.b.points = [p1,p2,p3]
        self.b.set_coeffs()
        self.assertEqual(self.b.coeffs,[1,3,3,1])

    def test_get_point(self):
        p1 = Point()
        p1.set(x=1,y=1)
        p2 = Point()
        p2.set(x=2,y=2)
        p3 = Point()
        p3.set(x=3, y=1)
        self.b.coeffs = [1,3,1]
        self.b.points = [p1,p2,p3]
        u = 0
        x = 0
        n = len(self.b.points)
        p = Point()
        p.set(x=0,y=0)
        while x <= n:
            u = x / float(n)
            p = self.b.get_point(u,x,p)
            print(p.get())
            x += 1
        
class Equation():
    def __init__(self):
        self.acceleration = GRAVITY
        self.velocity = None
        self.ux = None
        self.uy = None

    def set_equation(self,p1,p2,velocity):
        #percentage of the shot
        euclidean = math.sqrt(dx^2+dy^2)
        self.velocity = velocity
        vx = (dx/euclidean) * self.velocity
        vy = (dy/euclidean) * self.velocity
        if(vx > vy):
            #more hotizontal, less arc
            pass
        else:
            #more vertical, more arc
            pass

    def x_value(self,t):
        return self.x0 + self.ux*t
    
    def y_value(self,t):
        return self.y0 + self.uy*t - 1/2*self.acceleration*t^2

    def get_value(self,x):
        #kinematic equation d=vi*t + 1/2*a*t^2
        distance = self.velocity * x + 1/2*self.acceleration*x^2
        return distance
    
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
    
    def set_equation(self,p1, p2):
        '''
            a function that two sets of points for the cannon ball path
            Parameters:
                p1: a tuple of the point (x,y)
                p2: a tuple of the second point (x2,y2)
            Returns:
                True if set equation false otherwise
        '''
        equation = 0
        self.end = p1[0]

    def in_air(self):
        return self._shoot

    def increment(self):
        '''
        a function that moves the position of the cannonball
        '''
        self._time += 1

    def draw(self,pygame,screen):
        '''
        the function to draw the cannon
        Parameters:
            pygame: the pygame object
            screen: the screen to draw to
        Returns:
            None
        '''
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()