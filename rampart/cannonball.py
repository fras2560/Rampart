'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import math
import unittest
from explosion import Explosion
from point import Point
from color import Color
import pygame
import helper
from config import  GRAVITY
GRAVITY = -0.049

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
        self.velocity = 0
        self.y0 = 0
        self.time = 0
        self.step = 0
        self.x0 = 0
        self.vertical = False
        self.g = GRAVITY

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
        self.g = GRAVITY
        
    def set(self,p1,p2):
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
        dx = x2 - x1
        dy = y2 - y1
        self.y0 = y1
        self.x0 = x1
        top = float(y2) + 0.5*self.g * float(dx)*float(dx) - float(self.y0)
        self.velocity = top / float(dx)
        self.vertical  = False
        self.time = 0
        if dx < 0:
            #moving left
            self.step = -(1)
        elif dx > 0:
            #moving right
            self.step = (1)
        else:
            #just up/down
            self.step = (1)
            self.vertical = True
        return

    def get(self):
        '''
            a function that gets the current position of the equation
            Parameters:
                None:
            Returns:
                point: the current point (Point)
        '''
        t = self.time
        height = (-0.5*self.g*t*t + self.velocity*t + 
                  float(self.y0)) 
        point = Point()
        if not self.vertical:
            point.set(x=self.time+self.x0,y=height)
        else:
            point.set(x=self.x0,y=height)
        self.time += self.step
        return point

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
        fp = helper.file_path("cannonball.png", image=True)
        self.image = pygame.image.load(fp).convert()
        self.image.set_colorkey(self.color.black)
        self.rect = self.image.get_rect()
        self.bomb = Explosion()
        self.exploding = False

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
        self.rect.x = -1
        self.rect.y = -1
        self.exploding = False

    def set(self,p1, p2):
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
        self.exploding = False
        self.position = p1
        (x,y) = p1.get()
        self.rect.x = x
        self.rect.y = y
        
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
        self.position = self.equation.get()
        (x1,y1) = self.position.get()
        (x2,y2) = self.end.get()
        dx = x2 - x1
        dy = y2 - y1
        euclidean = math.sqrt(dx*dx + dy*dy)
        if self.past_end(x1,x2,self.equation.step):
            self.exploding = True
            self.bomb.set(self.end)
        return

    def past_end(self, a, b, direction):
        '''
        a function that checks if the a (point) is past the b point
        Parameters:
            a: the x coordinate of point
            b: the x coordinate of the second point
            direction: an int representing which direction the point is moving
        Returns:
            True if past
            False otherwise
        '''
        past = False
        print(a,b,direction)
        if a > b and direction > 0:
            past = True
        elif a < b and direction < 0:
            past = True
        return past
    
    def get(self):
        '''
        a function that gets position of the cannonball
        Parameters:
            None
        Returns:
            (x1,y1): a tuple fo the x and y position
        '''
        return self.position.get()
    
    def update(self):
        '''
        the function to update the cannonball position
        Parameters:
            none
        Returns:
            None
        '''
        if self._shoot and not self.exploding:
            self.increment()
            (x,y) = self.position.get()
            self.rect.x = x
            self.rect.y = y
    
    def draw(self, surface):
        '''
        a function to draw the cannonball or explosion
        Parameters:
            surface: the surface to draw on
        Returns:
            None
        '''
        if not self.exploding:
            surface_blit = surface.blit
            surface_blit(self.image, self.rect)
        else:
            self.bomb.update()
            self.bomb.draw(surface)
            if self.bomb.finished:
                self._shoot = False

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()