'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 01/05/2014
@note: This class is used to test Matrix and piece manually
'''
from rampart.level import Level
from rampart.player import Player
import pygame
from rampart.config import WATER, GRASS, CASTLE, NODE_SIZE, BASE
from rampart.color import Color
import os
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
        self.level = Level(BASE)
        self.done = False
        self.selected = 0
        self.players = [Player(iid=1, color=self.color.blue),
                        Player(iid=2, color=self.color.red)]
        self.player = self.players[0]
        self.save = os.path.join(os.path.dirname(BASE), 'output.txt')

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
        output = "Current selected player: " + str(self.player.get_id())
        label = self.point.render(output, 1, self.color.black)
        self.screen.blit(label,(SIZE[0] - MARGIN,y*LINE))
        y += 1

    def main(self):
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
                        self.player = self.players[0]
                    if key[pygame.K_2]:
                        self.player = self.players[1]
                    if key[pygame.K_s]:
                        self.level.save(self.save)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    if x < SIZE[0] - MARGIN and self.selected > 0:
                        if self.selected == CASTLE:
                            self.level.add_castle(x, y, self.player)
                            print("added castle")
                        else:
                            ratio = 2
                            x1 = x < SIZE[0] - MARGIN - (ratio+1) * NODE_SIZE
                            xcond =  x1 and x > ratio * NODE_SIZE
                            y1 = y < SIZE[1] - ratio * NODE_SIZE 
                            ycond = y > ratio * NODE_SIZE and  y1
                            if ycond and xcond:
                                self.level.update_node(x, y, self.selected)
            self.screen.fill(self.color.white)
            self.display_options()
            self.level.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test = Tester()
    test.main()