'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import helper
import pygame
from config import CASTLE, CANNON, LIVES, BUILDING, SHOOTING
from rampart.cannonball import Cannonball
from rampart.point import Point
from rampart.cursor import Cursor
from rampart.piece import Piece
from rampart.color import Color
class Player():
    def __init__(self, id=None, point=None, color=None):
        '''
        this class is used for player interactions
        Parameters:
            id: the player id (int)
            point: the starting point of the player's cursor
            color: the player's color
        Properties:
            cannonballs: a dictionary to hold all the players cannonsballs 
                        and what cannon shot the ball
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
        self.cursor = Cursor()
        if point is None:
            point = Point()
            point.set(0, 0)
        self.cursor.set(point)
        self.piece = Piece()
        self.piece.create_piece()
        self.mode = BUILDING
        if color is None:
            color = Color().blue
        self.color = color

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
        a method to draw all the cannonballs of the player or the player's
        piece depending on the mode
        Parameters:
            surface: the pygame display screen to draw on (surface)
        Returns:
            None
        '''
        if self.mode == SHOOTING:
            for ball in self.cannonballs:
                self.cannonballs[ball].draw(surface)
            self.cursor.draw(surface)
        else:
            self.piece.draw(surface, self.color)

    def shoot(self):
        '''
        a method for the player to shoot a cannonball at the specific position
        Parameters:
            None
        Returns:
            shot: True if able to shoot cannonball False otherwise (boolean)
        '''
        shot = False
        if self.mode == SHOOTING:
            for cannon in self.guns:
                position = cannon.get()
                if position not in self.cannonballs:
                    ball = Cannonball()
                    p1 = Point()
                    p1.set(position[0], position[1])
                    p2 = Point()
                    x, y = self.cursor.get()
                    p2.set(x, y)
                    ball.set(p1, p2)
                    self.cannonballs[position] = ball
                    shot = True
                    break
        return shot

    def move(self, horizontal=0, vertical=0):
        if self.mode == SHOOTING:
            self.cursor.move(horizontal, vertical)
        elif self.mode == BUILDING:
            self.piece.translate(horizontal, vertical)

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

    def get_piece(self):
        '''
        a method to get the player's piece
        Parameters:
            None
        Returns:
            self.piece: the player's piece
        '''
        return self.piece

    def shoot_mode(self):
        '''
        a method use to change the player's mode to shooing
        Parameters:
            None
        Returns:
            None
        '''
        self.mode = SHOOTING

    def build_mode(self):
        '''
        a method use to change the player's mode to building
        Parameters:
            None
        Returns:
            None
        '''
        self.mode = BUILDING

import unittest
from graph.node import Node
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
        self.player.shoot_mode()
        self.player.draw(self.screen)

    def testShoot(self):
        self.addCannon()
        self.addCannon(x=10, y=10)
        noshot = self.player.shoot()
        self.assertEqual(noshot, False)
        self.player.shoot_mode()
        self.player.move(10, 0)
        shot1 = self.player.shoot()
        self.player.move(90, 90)
        shot2 = self.player.shoot()
        self.player.move(-80, -80)
        shot3 = self.player.shoot()
        self.assertEqual(shot1, True)
        self.assertEqual(shot2, True)
        self.assertEqual(shot3, False)

    def testUpdate(self):
        self.player.shoot_mode()
        self.addCannon()
        self.addCannon(x=10, y=10)
        self.player.move(10, 10)
        shot1 = self.player.shoot()
        delete = self.player.update()
        while delete == []:
            self.player.draw(self.screen)
            delete = self.player.update()
        self.assertEqual(delete, [(10, 10.0)])
