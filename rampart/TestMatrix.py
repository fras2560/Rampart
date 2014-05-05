'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 01/05/2014
@note: This class is used to test Matrix and piece manually
'''
from rampart import Rampart
from piece import Piece
import pygame
from config import UP, DOWN, LEFT, RIGHT, WATER, GRASS, CANNON
from color import Color
SIZE = (500,500)
class Tester():
    def __init__(self):
        self.screen = None
        self.color = Color()
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Map Editor")
        pygame.key.set_repeat(1,10)
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 18)
        self.clock = pygame.time.Clock()
        self.speed = 1
        self.rampart = Rampart()
        self.done = False
        self.selected = 0
    
    def update_square(self, x,y):
        if self.selected > 0:
            self.rampart.game.update_square(x,y,self.selected)

    def main(self):
        self.rampart.game.load_level("test.txt")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_1]:
                        self.selected = GRASS
                    if key[pygame.K_2]:
                        self.selected = WATER
                    if key[pygame.K_3]:
                        self.selected = CANNON
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    self.update_square(x, y)
            self.screen.fill(self.color.white)
            self.rampart.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()