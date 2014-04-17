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
        (xi,yi) = point.get()
        point.set(x=int(round(xi,0)), y=int(round(yi,0)))
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
        self.assertEqual(self.b.coeffs,[1,2,1])

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
        self.assertEqual(p0.get(),(1,1))
        self.assertEqual(p1.get(),(2,2))
        self.assertEqual(p2.get(),(3,2.0))
        self.assertEqual(p3.get(),(3,2))
        self.assertEqual(p4.get(),(3,1))

class Equation():
    def __init__(self):
        self.bezier = Bezier()
        self.u = 0
        self.step = 0
        self.tol = 4
        self.done = False

    def in_range(self,p,p2):
        r = False
        if p < p2:
            if p2 + self.tol >= p:
                r = True
        elif p > p2:
            if p2-self.tol <= p:
                r = True
        return r

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
        euclidean = int(math.sqrt(dx*dx+dy*dy))
        if (dx < euclidean/2 and not self.in_range(dx, dy)):
            mid_y = (y1+y2) / 2
            mid_x = min(x1,x2) + euclidean
        elif (dy < euclidean/2 and not self.in_range(dy, dx)):
            mid_x = (x1 + x2) / 2
            mid_y = max(y1,y2) + euclidean
        elif dy < euclidean/2 and dx < euclidean/2:
            mid_x = min(x1,x2) + int(euclidean/2)
            mid_y = max(y1,y2) + int(euclidean/2)
        else:
            mid_x = min(x1,x2) + int(euclidean/4)
            mid_y = max(y1,y2) + int(euclidean/4)
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
        self.assertEqual(points[1].get(),(1,1))
        self.assertEqual(points[2].get(),(3,1))
        self.assertEqual(self.e.get().get(), (1.0,1.0))
        self.assertEqual(self.e.get().get(), (2,1))
        self.assertEqual(self.e.get().get(), (3.0,1.0))
        self.assertEqual(self.e.is_done(),True)
    
    def test_set_equation(self):
        p = Point()
        p.set(x=1,y=1)
        p2 = Point()
        p2.set(x=3,y=1)
        self.e.set_equation(p, p2)
        self.assertEqual(self.e.step, 0.5)
        points = self.e.bezier.points
        self.assertEqual(points[0].get(),(1,1))
        self.assertEqual(points[1].get(),(1,1))
        self.assertEqual(points[2].get(),(3,1))
        self.assertEqual(self.e.get().get(), (1,1))
        self.assertEqual(self.e.get().get(), (2,1))
        self.assertEqual(self.e.get().get(), (3,1))
        self.assertEqual(self.e.is_done(),True)

    def test_2_set_equation(self):
        p = Point()
        p.set(x=0,y=0)
        p2 = Point()
        p2.set(x=3,y=10)
        self.e.set_equation(p, p2)
        self.assertEqual(self.e.step, 0.1)
        points = self.e.bezier.points
        self.assertEqual(points[0].get(),(0,0))
        self.assertEqual(points[1].get(),(2,12))
        self.assertEqual(points[2].get(),(3,10))
        self.assertEqual(self.e.get().get(), (0.0,0.0))
        self.assertEqual(self.e.get().get(), (0,2))
        self.assertEqual(self.e.get().get(), (1,4))
        self.assertEqual(self.e.get().get(), (1,6))
        self.assertEqual(self.e.get().get(), (1,7))
        self.assertEqual(self.e.get().get(), (2,9))
        self.assertEqual(self.e.get().get(), (2,9))
        self.assertEqual(self.e.get().get(), (2,10))
        self.assertEqual(self.e.get().get(), (3,10))
        self.assertEqual(self.e.get().get(), (3,10))
        self.assertEqual(self.e.get().get(), (3,10))
        self.assertEqual(self.e.is_done(),True) 

    def test_3_set_equation(self):
        p = Point()
        p.set(x=0,y=0)
        p2 = Point()
        p2.set(x=3,y=10)
        self.e.set_equation(p2, p)
        self.assertEqual(self.e.step, 0.1)
        points = self.e.bezier.points
        self.assertEqual(points[0].get(),(3,10))
        self.assertEqual(points[1].get(),(2,12))
        self.assertEqual(points[2].get(),(0,0))
        self.assertEqual(self.e.get().get(), (3,10))
        self.assertEqual(self.e.get().get(), (3,10))
        self.assertEqual(self.e.get().get(), (3,10))
        self.assertEqual(self.e.get().get(), (2,10))
        self.assertEqual(self.e.get().get(), (2,9))
        self.assertEqual(self.e.get().get(), (2,9))
        self.assertEqual(self.e.get().get(), (1,7))
        self.assertEqual(self.e.get().get(), (1,6))
        self.assertEqual(self.e.get().get(), (1,4))
        self.assertEqual(self.e.get().get(), (0,2))
        self.assertEqual(self.e.get().get(), (0,0))
        self.assertEqual(self.e.is_done(),True) 

class Equation_2():
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

class TestEquation2(unittest.TestCase):
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
        self.equation = Equation_2()
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