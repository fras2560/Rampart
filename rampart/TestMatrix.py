'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 01/05/2014
@note: This class is used to test Matrix and piece manually
'''
from rampart import Rampart
from piece import Piece
from point import Point
import pygame
from config import UP, DOWN, LEFT, RIGHT, WATER, GRASS, CASTLE, TERRAIN
from color import Color
SIZE = (700,500)
MARGIN = 190
LINE = 10
BULLET = 5
class Tester():
    def __init__(self):
        self.screen = None
        self.color = Color()
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Map Editor")
        pygame.key.set_repeat(1,10)
        self.header = pygame.font.SysFont("monospace", 36)
        self.point = pygame.font.SysFont('monospace', 12)
        self.clock = pygame.time.Clock()
        self.speed = 1
        self.rampart = Rampart()
        self.done = False
        self.selected = 0
        self.player = 0

    def update_square(self, x,y):
        c1 = self.selected > 0
        c2 = x <= 500 - TERRAIN
        c3 = x > TERRAIN
        c4 = y > TERRAIN
        c5 = y < 500 - TERRAIN
        p = Point()
        p.set(x=x, y=y)
        if  c1 and c2  and c3 and c4 and c5:
            self.rampart.add(self.selected, p, self.player)

    def display_options(self):
        y = 1
        if self.selected == GRASS:
            output = "Selected: Grass"
        elif self.selected == WATER:
            output = "Selected: Water"
        elif self.selected == CASTLE:
            output = "Selected: Castle"
        else:
            output = "Selected: Nothing"
        label = self.point.render(output, 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN, y*LINE))
        y += 1
        label = self.point.render("Press Key to select:", 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN, y*LINE))
        y += 1
        label = self.point.render("G - Grass", 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN+BULLET, y*LINE))
        y += 1
        label = self.point.render("W - Water", 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN+BULLET, y*LINE))
        y += 1
        label = self.point.render("C - Castle", 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN+BULLET, y*LINE))
        y += 1
        label = self.point.render("Press s to Save to File", 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN, y*LINE))
        y += 1
        if self.player > 0:
            output = "Current selected player" + str(self.player)
            label = self.point.render(output, 1, self.color.black)
            self.screen.blit(label,(SIZE[0] - MARGIN,y*LINE))
        else:
            label = self.point.render("No selected player", 1, self.color.black)
            self.screen.blit(label,(SIZE[0] - MARGIN, y*LINE))
        y += 1

    def main(self):
        self.rampart.game.load_level("test.txt")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_g]:
                        self.selected = GRASS
                    if key[pygame.K_w]:
                        self.selected = WATER
                    if key[pygame.K_c]:
                        self.selected = CASTLE
                    if key[pygame.K_1]:
                        self.player = 1
                    if key[pygame.K_2]:
                        self.player = 2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    self.update_square(x, y)
            self.screen.fill(self.color.white)
            self.display_options()
            self.rampart.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()