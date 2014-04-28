'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used to test Cannonball manually
'''
import pygame
from cannonball import  Cannonball
from cursor import Cursor
from point import Point
SIZE = (500,500)
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
DOWN = 1
UP = -1
LEFT = -1
RIGHT = 1
class Tester():
    def __init__(self):
        self.screen = None
        
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Cannon Shoot")
        pygame.key.set_repeat(1,10)
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 18)
        self.center = Point()
        self.center.set(x=SIZE[0]/2, y=SIZE[1]/2)
        self.clock = pygame.time.Clock()
        self.ball = Cannonball()
        self.cursor = Cursor()
        self.cursor.set(self.center)
        self.speed = 1

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
                        if not self.ball.in_air():
                            (pos_x, pos_y) = self.cursor.get()
                            point = Point()
                            point.set(x=pos_x,y=pos_y)
                            self.ball.reset()
                            self.ball.set(self.center,point)
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
            self.screen.fill(WHITE)
            if self.ball.in_air():
                self.ball.update()
                self.ball.draw(self.screen)
            self.cursor.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()