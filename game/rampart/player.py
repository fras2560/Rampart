'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used for rampart game
'''
import pygame
'''
-------------------------------------------------------------------------------
All constants from config
-------------------------------------------------------------------------------
'''
from rampart.config import CASTLE, CANNON, LIVES, BUILDING, PLACING
from rampart.config import SHOOTING, NOMODE, NODE_SIZE, ROTATE_RIGHT
from rampart.config import SHOOT, MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT
from rampart.config import UP, DOWN, LEFT, RIGHT, LAY_PIECE, SPEED, ROTATE_LEFT
'''
-------------------------------------------------------------------------------
'''
from rampart.cannonball import Cannonball
from rampart.point import Point
from rampart.cursor import Cursor
from rampart.piece import Piece
from rampart.color import Color
from rampart.castle_draw import draw_castle

class Player():
    def __init__(self, iid=None, point=None, color=None):
        '''
        this class is used for player interactions
        Parameters:
            iid: the player id (int)
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
        if iid is None:
            iid = 1
        self.id = iid
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
        self.controls = {}
        self.available_cannons = 0
        self.point = pygame.font.SysFont('monospace', 12)
        self.black = Color().black

    def set_point(self, castle=0):
        '''
        a method that sets the initial point of the player equal to one
        of their castles
        Parameters:
            castle: the castle index to set the point to (int)
        Returns:
            None
        '''
        assert castle < len(self.towers), "Invalid Castle Index"
        (x, y) = self.towers[castle].get()
        p = Point()
        p.set(x, y)
        self.cursor.set(p)
        self.piece.translate(x, y)

    def check_castles(self):
        for tower in self.towers:
            if not tower.is_painted():
                self.available_cannons += 1

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
            add:True if added, False otherwise (boolean)
        '''
        add = True
        for tower in self.towers:
            if self.adjacent(tower.get(), castle.get()):
                add = False
                break
        if add:
            self.towers.append(castle)
        return add

    def adjacent(self, p1, p2):
        '''
        a method that determines if the two points are adjacent
        Parameters:
            p1: the first point (x,y)
            p2: the second point (x,y)
        Returns:
            pair: True if adjacent, False otherwise (boolean)
        '''
        xcond = abs(p1[0] - p2[0]) <= 2 * NODE_SIZE
        ycond = abs(p1[1] - p2[1]) <= NODE_SIZE
        return xcond and ycond

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
        for castle in self.towers:
            (x, y) = castle.get()
            draw_castle(surface, x, y, self.color)
        if self.mode == SHOOTING:
            for ball in self.cannonballs:
                self.cannonballs[ball].draw(surface)
            self.cursor.draw(surface)
        elif self.mode == BUILDING:
            self.piece.draw(surface, self.color)
        elif self.mode == PLACING:
            (x, y) = self.cursor.get()
            r = (x, y, NODE_SIZE, NODE_SIZE)
            pygame.draw.rect(surface, self.color, r, 2)
            label = self.point.render("%d" % (self.available_cannons),
                                  2, self.black)
            (x, y) = self.cursor.get()
            surface.blit(label, (x, y))

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
                if not cannon.is_painted() and position not in self.cannonballs:
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
        '''
        a method to move the player's piece or cursor
        Parameters:
            horizontal: the movement in the horizon (int)
            vertical: the movement in the vertical (int)
        Returns:
            None
        '''
        if self.mode == SHOOTING:
            self.cursor.move(horizontal, vertical)
        elif self.mode == BUILDING:
            self.piece.translate(horizontal, vertical)
        elif self.mode == PLACING:
            self.cursor.move(horizontal, vertical)

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
            nodes.append(self.cannonballs[ball].get_end())
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

    def normal_mode(self):
        '''
        a method used to change the player's mode to normal
        Parameters:
            None
        Returns:
            None
        '''
        self.mode = NOMODE

    def place_mode(self):
        '''
        a method used to change the player's mode to placing (cannons)
        Parameters:
            None
        Returns:
            None
        '''
        self.mode = PLACING

    def set_controls(self, controls):
        '''
        a method that sets the player controls
        Parameters:
            controls: a dictionary mapping key to event (dict)
        Returns:
            None
        '''
        self.controls = controls

    def player_control(self, keys, level):
        '''
        a method that takes the key presses and determines the player move
        Parameters:
            keys: the keys pressed
            level: the game level
        Returns:
            None
        '''
        for action, button in self.controls.items():
            if keys[button]:
                if self.mode == SHOOTING:
                    if action == SHOOT:
                        self.shoot()
                elif self.mode == BUILDING:
                    if action == LAY_PIECE:
                        added = level.add_piece(self)
                        if added:
                            pos = self.piece.return_points()[0]
                            self.piece.create_piece()
                            self.piece.translate(pos[0], pos[1])
                    elif action == ROTATE_RIGHT:
                        self.piece.clockwise_turn()
                    elif action == ROTATE_LEFT:
                        self.piece.counter_clockwise_turn()
                elif self.mode == PLACING:
                    if action == LAY_PIECE and self.available_cannons > 0:
                        (x, y) = self.cursor.get()
                        added = level.add_cannon(x, y, self)
                        if added:
                            self.available_cannons -= 1
                if action == MOVE_UP:
                    self.move(vertical = UP * SPEED)
                elif action == MOVE_DOWN:
                    self.move(vertical = DOWN * SPEED)
                elif action == MOVE_RIGHT:
                    self.move(horizontal = RIGHT * SPEED)
                elif action == MOVE_LEFT: 
                    self.move(horizontal = LEFT * SPEED)
        return

import unittest
from graph.node import Node
from graph.terrain import Terrain
from rampart.config import TERRAIN_TO_FILE, BACKGROUND, GRASS, BLOCK
from rampart.level import Level
import os
import logging
class PlayerTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Test Player Object")
        self.color = Color()
        self.screen.fill(self.color.white)
        self.terrain = Terrain(TERRAIN_TO_FILE, NODE_SIZE, BACKGROUND)
        self.player = Player()

    def tearDown(self):
        pygame.quit()

    def testReset(self):
        pass

    def addCastle(self):
        x = 0
        y = 0
        castle = Node(x=x, y=y, terrain=CASTLE,
                      player=1, images=self.terrain)
        added = self.player.add_castle(castle)
        self.assertEqual(added, True)
        added = self.player.add_castle(castle)
        self.assertEqual(added, False)

    def testAdjacent(self):
        result = self.player.adjacent((0,0), (0,0))
        self.assertEqual(True, result)
        result = self.player.adjacent((0,0), (10,0))
        self.assertEqual(True, result)
        result = self.player.adjacent((0,0), (0,10))
        self.assertEqual(True, result)
        result = self.player.adjacent((0,0), (10,10))
        self.assertEqual(True, result)
        result = self.player.adjacent((0,0), (21,0))
        self.assertEqual(False, result)
        result = self.player.adjacent((0,0), (0,21))
        self.assertEqual(False, result)
        result = self.player.adjacent((0,0), (21,21))
        self.assertEqual(False, result)

    def addCannon(self, x=None, y=None):
        if x is None:
            x = 0
        if y is None:
            y = 0
        cannon = Node(x=x, y=y, terrain=CANNON,
                      player=1, images=self.terrain)
        self.player.add_cannon(cannon)

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
        # initally painted (not available)
        noshot = self.player.shoot()
        self.assertEqual(noshot, False)
        self.player.shoot_mode()
        self.player.move(10, 0)
        noshot = self.player.shoot()
        self.assertEqual(noshot, False)
        # now unpaint them
        for cannon in self.player.guns:
            cannon.unpaint()
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
        # now unpaint them
        for cannon in self.player.guns:
            cannon.unpaint()
        self.player.move(10, 10)
        __shot1 = self.player.shoot()
        delete = self.player.update()
        while delete == []:
            self.player.draw(self.screen)
            delete = self.player.update()
        self.assertNotEqual(delete, [(0, 0)])

class PlayerControlTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Test Player Object")
        self.color = Color()
        self.screen.fill(self.color.white)
        self.terrain = Terrain(TERRAIN_TO_FILE, NODE_SIZE, BACKGROUND)
        self.player = Player()
        directory = os.path.dirname(os.getcwd())
        self.directory = os.path.join(directory, 'levels')
        self.fp = os.path.join(self.directory, 'test.txt')
        self.level = Level(self.fp, logger=self.logger, testing=True)
        controls = {
                    MOVE_UP: pygame.K_UP,
                    MOVE_DOWN: pygame.K_DOWN,
                    MOVE_RIGHT: pygame.K_RIGHT,
                    MOVE_LEFT: pygame.K_LEFT,
                    SHOOT: pygame.K_w,
                    LAY_PIECE: pygame.K_w,
                    ROTATE_RIGHT: pygame.K_d,
                    ROTATE_LEFT: pygame.K_a
                    }
        self.player.set_controls(controls)
        self.keys = [
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0
                     ]

    def testMovePieceUp(self):
        self.keys[pygame.K_UP] = 1
        before = self.player.piece.return_points()
        self.player.player_control(self.keys, self.level)
        result = self.player.piece.return_points()
        self.assertNotEqual(before, result)
        for i in range(0, len(result)):
            self.assertEqual(before[i][1] + UP * SPEED, result[i][1])

    def testMovePieceDown(self):
        self.keys[pygame.K_DOWN] = 1
        before = self.player.piece.return_points()
        self.player.player_control(self.keys, self.level)
        result = self.player.piece.return_points()
        self.assertNotEqual(before, result)
        for i in range(0, len(result)):
            self.assertEqual(before[i][1] + DOWN * SPEED, result[i][1])

    def testMovePieceLeft(self):
        self.keys[pygame.K_LEFT] = 1
        before = self.player.piece.return_points()
        self.player.player_control(self.keys, self.level)
        result = self.player.piece.return_points()
        self.assertNotEqual(before, result)
        for i in range(0, len(result)):
            self.assertEqual(before[i][0] + LEFT * SPEED, result[i][0])

    def testMovePieceRight(self):
        self.keys[pygame.K_RIGHT] = 1
        before = self.player.piece.return_points()
        self.player.player_control(self.keys, self.level)
        result = self.player.piece.return_points()
        self.assertNotEqual(before, result)
        for i in range(0, len(result)):
            self.assertEqual(before[i][0] + RIGHT * SPEED, result[i][0])

    def testMoveCursor(self):
        start = self.player.cursor.get()
        # move it up
        self.player.shoot_mode()
        before = self.player.cursor.get()
        self.keys[pygame.K_UP] = 1
        self.player.player_control(self.keys, self.level)
        result = self.player.cursor.get()
        self.assertNotEqual(before, result)
        self.assertEqual(before[1] + UP * SPEED, result[1])
        # move it down
        before = self.player.cursor.get()
        self.keys[pygame.K_UP] = 0
        self.keys[pygame.K_DOWN] = 1
        self.player.player_control(self.keys, self.level)
        result = self.player.cursor.get()
        self.assertNotEqual(before, result)
        self.assertEqual(before[1] + DOWN * SPEED, result[1])
        # move it right
        before = self.player.cursor.get()
        self.keys[pygame.K_DOWN] = 0
        self.keys[pygame.K_RIGHT] = 1
        self.player.player_control(self.keys, self.level)
        result = self.player.cursor.get()
        self.assertNotEqual(before, result)
        self.assertEqual(before[0] + RIGHT * SPEED, result[0])
        #move it left
        before = self.player.cursor.get()
        self.keys[pygame.K_RIGHT] = 0
        self.keys[pygame.K_LEFT] = 1
        self.player.player_control(self.keys, self.level)
        result = self.player.cursor.get()
        self.assertNotEqual(before, result)
        self.assertEqual(before[0] + LEFT * SPEED, result[0])
        self.assertEqual(start, result)

    def testShoot(self):
        self.player.cursor.move(0, 10)
        self.player.shoot_mode()
        self.keys[pygame.K_w] = 1
        self.player.player_control(self.keys, self.level)
        self.assertEqual({}, self.player.cannonballs)
        castle = Node(x=0, y=0, terrain=CANNON,
                      player=1, images=self.terrain)
        self.player.add_cannon(castle)
        self.player.player_control(self.keys, self.level)
        expect = {}
        expect[(0, 0)] = self.player.cannonballs[(0, 0)]
        self.assertEqual(expect, self.player.cannonballs)

    def testRotate(self):
        # rotate right
        self.player.build_mode()
        self.keys[pygame.K_d] = 1
        self.player.piece.reset()
        self.player.piece._L_piece()
        before = self.player.piece.return_points()
        self.player.player_control(self.keys, self.level)
        after = self.player.piece.return_points()
        self.assertNotEqual(before, after)
        expect = [(0, 0), (-10, 0), (10, 0), (-10, -10)]
        self.assertEqual(expect, after)
        # rotate back
        self.keys[pygame.K_d] = 0
        self.keys[pygame.K_a] = 1
        self.player.player_control(self.keys, self.level)
        final_pos = self.player.piece.return_points()
        self.assertNotEqual(final_pos, after)
        self.assertEqual(final_pos, before)

    def testLay(self):
        self.player.build_mode()
        self.keys[pygame.K_w] = 1
        self.player.piece.reset()
        self.player.piece._O_piece()
        self.player.player_control(self.keys, self.level)
        test = self.level.graph.get_node(0, 0)
        self.assertEqual(test.get_type(), BLOCK)
        self.assertNotEqual(test.get_type(), GRASS)

    def testAddCastle(self):
        self.player.place_mode()
        self.keys[pygame.K_w] = 1
        self.player.cursor.move(10, 10)
        self.player.player_control(self.keys, self.level)
        

