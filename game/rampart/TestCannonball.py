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
from graph.node import Node
from cursor import Cursor
from point import Point
from color import Color
from config import  DOWN, UP, LEFT, RIGHT, BASE, NODE_SIZE, CANNON
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
        self.cursor = Cursor()
        self.cursor.set(self.center)
        self.speed = 1
        self.level = Level(BASE)
        self.player = Player(1)
        self.level.add_cannon(250, 250, self.player)
        self.level.add_cannon(260, 250, self.player)
        
        
    def main(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        x, y = self.cursor.get()
                        self.player.shoot(x, y)
                    if key[pygame.K_s]:
                        self.speed = 10
                    else:
                        self.speed = 1
                    if key[pygame.K_UP]:
                        self.cursor.move(vertical=self.speed*UP)
                    if key[pygame.K_DOWN]:
                        self.cursor.move(vertical=self.speed*DOWN)
                    if key[pygame.K_RIGHT]:
                        self.cursor.move(horizontal=self.speed*RIGHT)
                    if key[pygame.K_LEFT]:
                        self.cursor.move(horizontal=self.speed*LEFT)
            self.screen.fill(self.color.white)
            self.player.update()
            self.level.draw(self.screen)
            self.player.draw(self.screen)
            self.cursor.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()