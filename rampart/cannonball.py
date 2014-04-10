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
        '''
        a function to add a control point to the bezier curve
        Parameters:
            point: the point to add (Point)
        Returns:
            None
        '''
        self.points.append(point)

    def set_coeffs(self):
        '''
        a function that set the coefficients for the blending function
        Parameters:
            None
        Returns:
            None
        '''
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

    def get_point(self,u):
        '''
        a function that calculate the bezier point
        Parameters:
            u: the value of u for blending function (p1=0<=u<=1.0=pn) (float)
        Returns:
            point: an object with the x and  position (Point)
        '''
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
    
    def print_points(self):
        '''
        a function that points the bezier points
        '''
        print("Bezier Points\n----------------------------")
        for point in self.points:
            print(point.get())
        print("----------------------------")
    
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
        p0 = self.b.get_point(0.0)
        p1 = self.b.get_point(0.25)
        p2 = self.b.get_point(0.5)
        p3 = self.b.get_point(0.75)
        p4 = self.b.get_point(1.0)
        self.assertEqual(p0.get(),(1.0,1.0))
        self.assertEqual(p1.get(),(1.875,1.75))
        self.assertEqual(p2.get(),(2.5,2.0))
        self.assertEqual(p3.get(),(2.875,1.75))
        self.assertEqual(p4.get(),(3.0,1.0))

class Equation():
    def __init__(self):
        self.bezier = Bezier()
        self.u = 0
        self.step = 0
        self.tol = 10
        self.done = False

    def set_equation(self,p1,p2):
        '''
        a function that takes two points and creates the bezier equation
        Parameters:
            p1: the first point (Point)
            p2: the second point (Point)
        Returns:
            None
        '''
        (x1,y1) = p1.get()
        (x2,y2) = p2.get()
        dx = math.fabs(x1 - x2)
        dy = math.fabs(y1 - y2)
        euclidean = math.sqrt(dx*dx+dy*dy)
        if (dx < self.tol and dx < dy/2):
            mid_y = (y1+y2) / 2
            mid_x = min(x1,x2) + euclidean
        else:
            mid_x = (x1 + x2) / 2
            mid_y = min(y1,y2) + euclidean
        #set the the step size
        self.step = 1 / float(euclidean)
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
        a function that returns the current points and moves to the next point
        Parameters:
            None
        Returns:
            p: the point (Point)
        '''
        p = self.bezier.get_point(self.u)
        
        self.u += self.step
        if(self.u >= 1.0):
            self.done = True
        return p
    
    def is_done(self):
        '''
        a function tot check if the equation has got to the second point
        Parameters:
            None
        Returns:
            done: True if equation is done False otherwise
        '''
        return self.done

class TestEquation(unittest.TestCase):
    def setUp(self):
        self.e = Equation()

    def tearDown(self):
        pass
    
    def test_simple_set_equation(self):
        p = Point()
        p.set(x=1,y=1)
        p2 = Point()
        p2.set(x=3,y=1)
        self.e.set_equation(p, p2)
        self.assertEqual(self.e.step, 0.5)
        points = self.e.bezier.points
        self.assertEqual(points[0].get(),(1,1))
        self.assertEqual(points[1].get(),(2,3.0))
        self.assertEqual(points[2].get(),(3,1))
        self.assertEqual(self.e.get().get(), (1.0,1.0))
        self.assertEqual(self.e.get().get(), (2.0,2.0))
        self.assertEqual(self.e.get().get(), (3.0,1.0))
        self.assertEqual(self.e.is_done(),True)
    
    def test_simple_set_equation(self):
        p = Point()
        p.set(x=1,y=1)
        p2 = Point()
        p2.set(x=3,y=1)
        self.e.set_equation(p, p2)
        self.assertEqual(self.e.step, 0.5)
        points = self.e.bezier.points
        self.assertEqual(points[0].get(),(1,1))
        self.assertEqual(points[1].get(),(2,3.0))
        self.assertEqual(points[2].get(),(3,1))
        self.assertEqual(self.e.get().get(), (1.0,1.0))
        self.assertEqual(self.e.get().get(), (2.0,2.0))
        self.assertEqual(self.e.get().get(), (3.0,1.0))
        self.assertEqual(self.e.is_done(),True) 

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