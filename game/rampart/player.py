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
from rampart.point import Point
class Player():
    def __init__(self, id=None):
        '''
        this class is used for player interactions
        Parameters:
            id: the player id (int)
        Properties:
            cannonballs: a dictionary to hold all the players cannonsballs and what
                        cannon shot the ball
            guns: a list to hold all the players cannons (Node)
            towers: a list to hold all the towers: (Node)
            points: the number of points the player has (int)
            lives: the number of lives the player has (int)
        '''
        self.cannonballs = {}
        self.guns = []
        self.towers = []
        self.points = 0
        self.lives = LIVES
        if id is None:
            id = 1
        self.id = id

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
            self.cannonballs[ball].draw(surface)

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
                p1 = Point()
                p1.set(position[0], position[1])
                p2 = Point()
                p2.set(x, y)
                ball.set(p1, p2)
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
        for ball in self.cannonballs:
            self.cannonballs[ball].update()
            print(self.cannonballs[ball].get())
            if not self.cannonballs[ball].in_air():
                delete.append(ball)
        for ball in delete:
            nodes.append(self.cannonballs[ball].get())
            del self.cannonballs[ball]
        return nodes

    def get_id(self):
        '''
        a method to get the player id
        Parameters:
            None
        Returns:
            self.id: the player id (int)
        '''
        return self.id

import unittest
from rampart.color import Color
from graph.node import Node
from rampart.config import CASTLE, CANNON
class PlayerTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Test Player Object")
        self.color = Color()
        self.screen.fill(self.color.white)
        self.player = Player()

    def tearDown(self):
        pygame.quit()

    def testReset(self):
        pass

    def addCastle(self):
        x = 0
        y = 0
        castle = Node(x=x, y=y, image_file="castle.png", terrain=CASTLE,
                      player=1)
        self.player.add_castle(castle)

    def addCannon(self, x=None, y=None):
        if x is None:
            x = 0
        if y is None:
            y = 0
        castle = Node(x=x, y=y, image_file="cannon.png", terrain=CANNON,
                      player=1)
        self.player.add_cannon(castle)

    def testAddCastle(self):
        self.addCastle()
        self.assertEqual(len(self.player.towers), 1)

    def testAddCannon(self):
        self.addCannon()
        self.assertEqual(len(self.player.guns), 1)

    def testDraw(self):
        self.addCannon()
        self.addCastle()
        self.player.draw(self.screen)

    def testShoot(self):
        self.addCannon()
        self.addCannon(x=10, y=10)
        shot1 = self.player.shoot(10, 10)
        shot2 = self.player.shoot(100, 100)
        shot3 = self.player.shoot(20, 20)
        self.assertEqual(shot1, True)
        self.assertEqual(shot2, True)
        self.assertEqual(shot3, False)

    def testUpdate(self):
        self.addCannon()
        self.addCannon(x=10, y=10)
        shot1 = self.player.shoot(10, 10)
        delete = self.player.update()
        while delete == []:
            self.player.draw(self.screen)
            delete = self.player.update()
        self.assertEqual(delete, [(10, 10.0)])
