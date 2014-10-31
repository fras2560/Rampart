'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import helper
import pygame
from config import CASTLE, CANNON, LIVES
from rampart.cannonball import Cannonball
class Player():
    def __init__(self):
        '''
        this class is used for player interactions
        cannonballs: a dictionary to hold all the players cannonsballs and what
                    cannon shot the ball
        guns: a list to hold all the players cannons (Node)
        towers: a list to hold all the towers: (Node)
        points: the number of points the player has (int)
        lives: the number of lives the player has
        '''
        self.cannonballs = {}
        self.guns = []
        self.towers = []
        self.points = 0
        self.lives = LIVES

    def reset(self):
        '''
        a that resets the player
        Parameters:
            None
        Returns:
            None
        '''
        self.guns = []
        self.towers = []
        self.points = 0
        self.lives = LIVES

    def add_castle(self, castle):
        '''
        a method to add an castle to the player
        Parameters:
            castle: the castle node object (Node)
        Returns:
            None
        '''
        self.towers.append(castle)

    def add_cannon(self, cannon):
        '''
        a method to add a cannon to the player's arsenal
        Parameters:
            cannon: the cannon node object (Node)
        Returns:
            None
        '''
        self.guns.append(cannon)

    def draw(self, surface):
        '''
        a method to draw all the cannonballs of the player
        Parameters:
            surface: the pygame display screen to draw on (surface)
        Returns:
            None
        '''
        for ball in self.cannonballs:
            ball.draw(surface)

    def shoot(self, x, y):
        '''
        a method for the player to shoot a cannonball at the specific position
        Parameters:
            x: the x position to shoot for (int)
            y: the y position to shoot for (int)
        Returns:
            shot: True if able to shoot cannonball False otherwise (boolean)
        '''
        shot = False
        for cannon in self.guns:
            position = cannon.get()
            if position not in self.cannonballs:
                ball = Cannonball()
                ball.set(position, (x, y))
                self.cannonballs[position] = ball
                shot = True
                break
        return shot

    def update(self):
        ''''
        a method used to update the position of each cannonball
        Parameters:
            None
        Returns:
            nodes: the nodes of where the cannonball hit (list)
        '''
        delete = []
        nodes = []
        for ball in self.cannonballs.items():
            self.cannonballs[ball].update()
            if not self.cannonballs[ball].in_air():
                delete.append(ball)
        for ball in delete:
            nodes.append(self.cannonballs[ball].get())
            del self.cannonballs[ball]
        return nodes

