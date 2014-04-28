'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 06/04/2014
@note: This class is used to test Cannonball manually
'''
import pygame
from cannonball import  Cannonball
from explosion import Explosion
from point import Point
SIZE = (500,500)
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

class Tester():
    def __init__(self):
        self.screen = None
        
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Cannon Shoot")
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 18)
        self.center = Point()
        self.center.set(x=SIZE[0]/2, y=SIZE[1]/2)
        self.clock = pygame.time.Clock()

    def main(self):
        done = False
        sprites = pygame.sprite.Group()
        ball = None
        bomb = None
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if len(sprites) == 0:
                        point = Point()
                        point.set(x=pos[0],y=pos[1])
                        ball = Cannonball()
                        ball.set(self.center,point)
                        sprites.add(ball)
            self.screen.fill(WHITE)
            if ball is not None and not ball.in_air():
                sprites.empty()
                del ball
                ball = None
                bomb = Explosion()
                bomb.set(point)
                sprites.add(bomb)
            if bomb is not None and bomb.finished:
                sprites.empty()
                del bomb
                bomb = None
            sprites.update()
            sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()