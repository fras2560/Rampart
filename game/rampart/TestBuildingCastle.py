'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 10/27/2014
@note: Used to test the building process of rampart
'''
import pygame
from rampart.level import Level
from rampart.player import Player
from point import Point
from color import Color
from config import  DOWN, UP, LEFT, RIGHT, BASE, NODE_SIZE
SIZE = (500,500)

class Tester():
    def __init__(self):
        self.screen = None
        self.color = Color()
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Test Building")
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
                    if key[pygame.K_SPACE]:
                        added = self.level.add_piece(self.player)
                        if added:
                            self.player.piece.create_piece()
                    if key[pygame.K_UP]:
                        self.player.move(vertical=UP*NODE_SIZE)
                    if key[pygame.K_DOWN]:
                        self.player.move(vertical=DOWN*NODE_SIZE)
                    if key[pygame.K_RIGHT]:
                        self.player.move(horizontal=RIGHT*NODE_SIZE)
                    if key[pygame.K_LEFT]:
                        self.player.move(horizontal=LEFT*NODE_SIZE)
                    if key[pygame.K_w]:
                        self.player.piece.counter_clockwise_turn()
                    if key[pygame.K_s]:
                        self.player.piece.clockwise_turn()
            self.screen.fill(self.color.white)
            self.player.update()
            self.level.draw(self.screen)
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    t = Tester()
    t.main()