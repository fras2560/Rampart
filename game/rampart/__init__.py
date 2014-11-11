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
from rampart.config import BASE, PLAYERCOLORS, BUILDING, SHOOTING
from rampart.config import BUILDTIME, SHOOTTIME, SIZE, NODE_SIZE
from rampart.config import LEFT, RIGHT, UP, DOWN

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
        logging.basicConfig(filename="rampart.log", level=logging.INFO,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.players = []
        for p_id in range(0, players):
            self.players.append(Player(iid=p_id, color=PLAYERCOLORS[p_id]))
        self.level = Level(level, logger=self.logger)
        self.mode = BUILDING
        self.time = BUILDTIME
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Building")
        pygame.key.set_repeat(1, 5)
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 18)

    def display_clock(self):
        label = self.point.render("Time: %d" % self.clock, 2, self.color.black)
        self.screen.blit(label,(SIZE[0] // 2, 2 * NODE_SIZE))

    def draw(self):
        self.level.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        self.display_clock()

    def controls(self):
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                keys.append(key)
        return
