'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
GRAVITY = -9.8

class Equation():
    def __init__(self):
        self.acceleration = GRAVITY
        self.velocity = None
        self.y1 = None
        

    def set_equation(self,interval,):
        passs

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
        self.equation = None
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