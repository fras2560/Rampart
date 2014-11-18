'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 10/27/2014
@note: The main of rampart
'''

'''
-------------------------------------------------------------------------------
Imports
-------------------------------------------------------------------------------
'''
from rampart.config import BASE, PLAYERCOLORS, BUILDING, SHOOTING, PLACING
from rampart.config import BUILDTIME, SHOOTTIME, PLACETIME, SIZE, NODE_SIZE
from rampart.config import LEFT, RIGHT, UP, DOWN, CLEANUP
from rampart.color import Color
from rampart.player import Player
from rampart.level import Level
import pygame
import logging

class Rampart():
    def __init__(self, players, level):
        '''
        Parameters:
            players: the number of players (int)
            level: the level to player (filepath)
        '''
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Rampart")
        pygame.key.set_repeat(1, 5)
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 18)
        self.color = Color()
        self.players = []
        self.level = Level(level, logger=self.logger)
        for p_id in range(1, players+1):
            self.players.append(Player(iid=p_id, color=PLAYERCOLORS[p_id - 1]))
            self.level.add_players_castles(self.players[p_id - 1])
        for p_id in range(1, players+1):
            self.players[p_id -1].set_point()
        self.build_mode()
        self.clock = BUILDTIME
        self.play = True
        self.heart = pygame.time.Clock()

    def display_clock(self):
        '''
            a method that display the game clock
            Parameters:
                None
            Returns:
                None
        '''
        label = self.point.render("Time: %d" % (self.clock //10),
                                  2, self.color.black)
        self.screen.blit(label,(SIZE[0] // 2, 2 * NODE_SIZE))

    def draw(self):
        '''
            a method that draw the game
            Parameters:
                None
            Returns:
                None
        '''
        self.screen.fill(self.color.white)
        self.level.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        self.display_clock()
        pygame.display.flip()

    def set_player_controls(self, player, controls):
        '''
            a method that set the player controls of a certain player
            Parameters:
                player: the player to set (int)
                controls: a dictionary of controls (dict)
            Returns:
                None
        '''
        self.players[player - 1].set_controls(controls)

    def controls(self):
        '''
            a method that deals with controls of the game
            Parameters:
                None
            Returns:
                None
        '''
        keys = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                keys = key
        if keys is not None:
            if self.mode != CLEANUP:
                for player in self.players:
                    player.player_control(keys, self.level)
        return

    def tick(self):
        '''
            a method that updates the clock of the game
            Parameters:
                None
            Returns:
                None
        '''
        self.clock -= 1
        if self.mode == BUILDING or self.mode == PLACING:
            self.level.update()
        for p in self.players:
            if self.mode == SHOOTING:
                balls = p.update()
                for ball in balls:
                    (x, y) = ball
                    self.logger.info("Destroyed (%d, %d)" % (x, y))
                    self.level.destroy_node(x, y)

    def cleanup(self):
        '''
            a method that cleans up the map after shooting has occurred
            Parameters:
                None
            Returns:
                None
        '''
        finish = True
        for player in self.players:
            if len(player.cannonballs) > 0:
                finish = False
            balls = player.update()
            for ball in balls:
                (x, y) = ball
                self.level.destroy_node(x, y)
        return finish

    def game_tick(self):
        '''
            a method that is the driving force behind the game
            Parameters:
                None
            Returns:
                True if game is still going, False otherwise (boolean)
        '''
        self.controls()
        if self.play:
            if self.mode != CLEANUP:
                self.tick()
            if self.clock == 0 and self.mode != CLEANUP:
                self.switch_mode()
            elif self.mode == CLEANUP:
                finished = self.cleanup()
                if finished:
                    self.level.cleanup()
                    self.build_mode()
            self.draw()
            self.heart.tick(10)
        return self.play

    def switch_mode(self):
        '''
            a method that switchs the mode to the mode
            Parameters:
                None
            Returns:
                None
        '''
        if self.mode == BUILDING:
            self.place_mode()
        elif self.mode == PLACING:
            self.shoot_mode()
        elif self.mode == SHOOTING:
            self.mode = CLEANUP

    def place_mode(self):
        '''
            a method that chanes the game to place mode
            Parameters:
                None
            Returns:
                None
        '''
        for player in self.players:
            player.place_mode()
            player.check_castles()
        self.clock = PLACETIME
        self.mode = PLACING

    def build_mode(self):
        '''
            a method that changes the game to build mode
            Parameters:
                None
            Returns:
                None
        '''
        for player in self.players:
            player.build_mode()
        self.clock = BUILDTIME
        self.mode = BUILDING

    def shoot_mode(self):
        '''
            a method that sets the game into shooting mode
            Parameters:
                None
            Returns:
                None
        '''
        for player in self.players:
            player.shoot_mode()
        self.clock = SHOOTTIME
        self.mode = SHOOTING

import unittest
from rampart.config import BUILDINGBASE
from config import MOVE_UP, MOVE_DOWN, MOVE_RIGHT, SHOOT, MOVE_LEFT
from config import LAY_PIECE, ROTATE_RIGHT, ROTATE_LEFT

class TestRampart(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        pygame.init()
        self.color = Color()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Test Rampart Object")
        self.screen.fill(self.color.white)
        self.rampart = Rampart(2, BUILDINGBASE)
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
        self.rampart.set_player_controls(0, controls)
        self.rampart.set_player_controls(1, {})
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

    def tearDown(self):
        pygame.quit()

    def testShootMode(self):
        # initialize to build mode
        self.rampart.shoot_mode()
        after_clock = self.rampart.clock
        self.assertEqual(after_clock, SHOOTTIME)
        for player in self.rampart.players:
            self.assertEqual(SHOOTING, player.mode)

    def testBuildMode(self):
        self.rampart.clock = 0
        for player in self.rampart.players:
            player.shoot_mode()
        self.rampart.build_mode()
        after_clock = self.rampart.clock
        self.assertEqual(after_clock, BUILDTIME)
        for player in self.rampart.players:
            self.assertEqual(BUILDING, player.mode)

    def testSwitchMode(self):
        # initialized to shoot
        before_type = self.rampart.players[0].mode
        before_clock = self.rampart.clock
        self.rampart.switch_mode()
        self.assertEqual(self.rampart.players[0].mode, SHOOTING)
        self.assertNotEqual(self.rampart.players[0].mode, before_type)
        self.assertEqual(self.rampart.clock, SHOOTTIME)
        self.assertNotEqual(self.rampart.clock, before_clock)
        # now switch back
        self.rampart.switch_mode()
        self.assertEqual(self.rampart.players[0].mode, before_type)
        self.assertNotEqual(self.rampart.players[0].mode, SHOOTING)
        self.assertEqual(self.rampart.clock, before_clock)
        self.assertNotEqual(self.rampart.clock, SHOOTTIME)
