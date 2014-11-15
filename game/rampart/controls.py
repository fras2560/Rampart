'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 11/15/2014
@note: This class holds the controls for the players
'''
from config import MOVE_UP, MOVE_DOWN, MOVE_RIGHT, SHOOT, MOVE_LEFT
from config import LAY_PIECE, ROTATE_RIGHT, ROTATE_LEFT
import pygame
PLAYERONE = {
                MOVE_UP: pygame.K_UP,
                MOVE_DOWN: pygame.K_DOWN,
                MOVE_RIGHT: pygame.K_RIGHT,
                MOVE_LEFT: pygame.K_LEFT,
                SHOOT: pygame.K_w,
                LAY_PIECE: pygame.K_w,
                ROTATE_RIGHT: pygame.K_d,
                ROTATE_LEFT: pygame.K_a
            }
