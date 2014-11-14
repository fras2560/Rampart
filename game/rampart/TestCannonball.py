'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used to test Cannonball manually
'''
import pygame
from rampart.level import Level
from rampart.player import Player
from point import Point
from color import Color
from config import  DOWN, UP, LEFT, RIGHT, BASE
from config import MOVE_UP, MOVE_DOWN, MOVE_RIGHT, SHOOT, MOVE_LEFT
from config import LAY_PIECE, ROTATE_RIGHT, ROTATE_LEFT

SIZE = (500,500)
class Tester():
    def __init__(self):
        self.screen = None
        self.color = Color()
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Cannon Shoot")
        pygame.key.set_repeat(1,10)
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 18)
        self.center = Point()
        self.center.set(x=SIZE[0]/2, y=SIZE[1]/2)
        self.sec = Point()
        self.sec.set(x=SIZE[0]/2+15, y=SIZE[1]/2)
        self.clock = pygame.time.Clock()
        self.speed = 1
        self.level = Level(BASE)
        self.player = Player(1, self.center)
        self.player.shoot_mode()
        self.level.add_cannon(250, 250, self.player)
        self.level.add_cannon(260, 250, self.player)
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

    def main(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    __ = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    self.player.player_control(key, self.level)
            self.screen.fill(self.color.white)
            self.player.update()
            self.level.draw(self.screen)
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()