'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import pygame
import rampart.helper as helper
from rampart.color import Color

class Cursor(pygame.sprite.Sprite):
    def __init__(self, color=None):
        '''
        color: initializes the color of the cursor (RR, GG, BB)
        '''
        pygame.sprite.Sprite.__init__(self)
        self.colors = Color()
        if color is None:
            self.color = self.colors.blue
            
        
    def set(self, point):
        '''
        a method that sets the point of the cursor
        Parameters:
            point: the point of the cursor
        Returns:
            None
        '''
        (x, y) = point.get()
        self.x = x
        self.y = y
    
    def get(self):
        '''
        a method to get the position of the cursor
        Parameters:
            None
        Returns
            (x,y): the x and y position (tuple)
        '''
        return (self.x, self.y)
    
    def move(self, horizontal=0, vertical=0):
        '''
        a method to move the cursor
        Parameters:
            horizontal: the movement in the x axis
            vertical: the movement in the y axis
        Returns:
            None
        '''
        self.x += horizontal
        self.y += vertical

    def update(self):
        '''
        a method to update the cursor
        Parameters:
            None
        Returns:
            None
        '''
        pass

    def draw(self, surface):
        '''
        a method to draw the cursor
        Parameters:
            surface: the surface to draw on
        '''
        point = (int(self.x), int(self.y))
        # draw two circles
        pygame.draw.circle(surface, self.color,
                           point, 5, 1)
        pygame.draw.circle(surface, self.colors.black,
                           point, 2, 1)
        # draw cross hairs
        point2 = (int(self.x + 5), int(self.y))
        point3 = (int(self.x - 5), int(self.y))
        point4 = (int(self.x), int(self.y + 5))
        point5 = (int(self.x), int(self.y - 5))
        
        pygame.draw.line(surface, self.color, point, point2, 1)
        pygame.draw.line(surface, self.color, point, point3, 1)
        pygame.draw.line(surface, self.color, point, point4, 1)
        pygame.draw.line(surface, self.color, point, point5, 1)
        
