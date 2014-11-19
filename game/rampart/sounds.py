'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 11/18/2014
@note: a sounds object for all the sounds of the game
'''
import pygame
from rampart.helper import file_path
from rampart.config import CANNON_SOUNDS, APPLAUSE, END_TURN, WELCOME
from rampart.config import EXPLOSION_SOUNDS
from random import randint
class Sounds():
    def __init__(self):
        self._cannons = []
        self._explosions = []
        for cannon in CANNON_SOUNDS:
            fp = file_path(cannon, sound=True)
            self._cannons.append(pygame.mixer.Sound(fp))
        for explosion in EXPLOSION_SOUNDS:
            fp = file_path(explosion, sound=True)
            self._explosions.append(pygame.mixer.Sound(fp))
        fp = file_path(APPLAUSE, sound=True)
        self._applause = pygame.mixer.Sound(fp)
        fp = file_path(END_TURN, sound=True)
        self._end_turn = pygame.mixer.Sound(fp)
        fp = file_path(WELCOME, sound=True)
        self._welcome = pygame.mixer.Sound(fp)

    def explosion(self):
        '''
        a method that plays an explosion sound
        Parameters:
            None
        Returns:
            None
        '''
        sound = randint(0, len(self._explosions) - 1)
        self._explosions[sound].play()

    def cannon(self):
        '''
        a method that plays a cannon sound
        Parameters:
            None
        Returns:
            None
        '''
        sound = randint(0, len(self._cannons) - 1)
        self._cannons[sound].play()

    def applause(self):
        '''
        a method that plays an applause sound
        Parameters:
            None
        Returns:
            None
        '''
        self._applause.play()

    def end_turn(self):
        '''
        a method that plays a end of turn sound
        Parameters:
            None
        Returns:
            None
        '''
        self._end_turn.play()

    def welcome(self):
        '''
        a method that plays a welcome sound
        Parameters:
            None
        Returns:
            None
        '''
        self._welcome.play()

import unittest
class TestSounds(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.sound = Sounds()

    def tearDown(self):
        pygame.quit()

    def testSounds(self):
        self.sound.applause()
        self.sound.cannon()
        self.sound.end_turn()
        print(len(self.sound._cannons))
