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
                MOVE_UP: pygame.K_w,
                MOVE_DOWN: pygame.K_s,
                MOVE_RIGHT: pygame.K_d,
                MOVE_LEFT: pygame.K_a,
                SHOOT: pygame.K_g,
                LAY_PIECE: pygame.K_g,
                ROTATE_RIGHT: pygame.K_h,
                ROTATE_LEFT: pygame.K_j
            }
PLAYERTWO = {
                MOVE_UP: pygame.K_UP,
                MOVE_DOWN: pygame.K_DOWN,
                MOVE_RIGHT: pygame.K_RIGHT,
                MOVE_LEFT: pygame.K_LEFT,
                SHOOT: pygame.K_KP1,
                LAY_PIECE: pygame.K_KP1,
                ROTATE_RIGHT: pygame.K_KP2,
                ROTATE_LEFT: pygame.K_KP3
             }
