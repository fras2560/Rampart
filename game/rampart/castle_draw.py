'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 11/09/2014
@note: holds the function for drawing a castle
'''
import pygame
from rampart.config import NODE_SIZE
from rampart.color import Color
def draw_castle(surface, x, y, color):
    '''
    a function which draws a castle
    Parameters:
        surface: the surface upon which to draw
        x: the top left x position of the castle (int)
        y: the top left y position of the castle (int)
        color: the color of the accent (RR, GG, BB)
    Returns:
        None
    '''
    c = Color()
    xs = [x + i*NODE_SIZE for i in range(0, 4)]
    ys = [y + i*NODE_SIZE for i in range(0, 3)]
    TRIANGLE_HEIGHT = NODE_SIZE // 3
    CASTLE_WIDTH = NODE_SIZE // 2
    CASTLE_HEIGHT = (2 * NODE_SIZE) - TRIANGLE_HEIGHT
    CASTLE_HEIGHT = CASTLE_HEIGHT - (CASTLE_HEIGHT % 2)
    TRIANGLE_WIDTH = CASTLE_WIDTH
    # draw base
    r = (xs[0] + (CASTLE_WIDTH), ys[2] - CASTLE_HEIGHT//2,
                  CASTLE_WIDTH * 4, CASTLE_HEIGHT//2)
    pygame.draw.rect(surface, c.stone, r)
    pygame.draw.rect(surface, c.black, r, 1)
    r = (xs[0], ys[2] - CASTLE_HEIGHT,
         CASTLE_WIDTH, CASTLE_HEIGHT)
    pygame.draw.rect(surface, c.stone, r)
    pygame.draw.rect(surface, c.black, r, 1)
    r = (xs[3] - CASTLE_WIDTH, ys[2] - CASTLE_HEIGHT,
         CASTLE_WIDTH, CASTLE_HEIGHT)
    pygame.draw.rect(surface, c.stone, r)
    pygame.draw.rect(surface, c.black, r, 1)
    r = (xs[1] + CASTLE_WIDTH // 2, ys[2] - CASTLE_HEIGHT,
         CASTLE_WIDTH, CASTLE_HEIGHT//2)
    pygame.draw.rect(surface, c.stone, r)
    pygame.draw.rect(surface, c.black, r, 1)
    # draw castle points (triangles)
    pl = make_triangle(xs[0], ys[2] - CASTLE_HEIGHT,
                       TRIANGLE_HEIGHT, TRIANGLE_WIDTH)
    pygame.draw.polygon(surface, color, pl)
    outline_triangle(surface, pl, c.black)
    pl = make_triangle(xs[3] - CASTLE_WIDTH, ys[2] - CASTLE_HEIGHT,
                       TRIANGLE_HEIGHT, TRIANGLE_WIDTH)
    pygame.draw.polygon(surface, color, pl)
    outline_triangle(surface, pl, c.black)
    pl = make_triangle(xs[1] + CASTLE_WIDTH // 2, ys[2] - CASTLE_HEIGHT,
                       TRIANGLE_HEIGHT, TRIANGLE_WIDTH)
    pygame.draw.polygon(surface, color, pl)
    outline_triangle(surface, pl, c.black)
    # draw door
    r = (xs[1] + CASTLE_WIDTH // 2, ys[2] - 2 * TRIANGLE_HEIGHT,
         CASTLE_WIDTH, 2 * TRIANGLE_HEIGHT)
    pygame.draw.rect(surface, color, r)
    pygame.draw.rect(surface, color, r, 1)

def outline_triangle(surface, point_list, color):
    '''
    a function that draws a outline of a the triangle
    Parameters:
        surface: the surface to draw (surface)
        point_list: the three points of the triangle (list)
        color: the color of the outline (RR, GG, BB)
    Returns:
        None
    '''
    index = 0
    length = len(point_list)
    while index < length:
        start = point_list[index]
        end = point_list[(index + 1) % length]
        pygame.draw.line(surface, color, start, end)
        index += 1
    return

def make_triangle(x1, y1, height, width):
    '''
    a function which forms a triangle
    Parameters:
        x1: the left side of the triangle (int)
        y1: the lower side of the triangle (int)
        height: the height of the triangle (int)
        width: the width of the triagle (int)
    Returns:
        point_list: the list of points (list)
    '''
    point_list = []
    point_list.append((x1, y1))
    point_list.append((x1 + width // 2, y1 - height))
    point_list.append((x1 + width, y1))
    return point_list

def make_rect(x1, x2, y1, y2):
    '''
    a function which forms the rect
    Parameters:
        x1: the left x position (int)
        x2: the right x position (int)
        y1: the lower y position (int)
        y2: the upper y position (int)
    Returns:
        rect: (x, y, width, height)
    '''
    height = y1 - y2
    width = x2 - x1
    return (x1, y2, width, height)


import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.pygame = False
        self.color = Color()

    def tearDown(self):
        if self.pygame:
            pygame.quit()

    def testCastleDraw(self):
        self.pygame = True
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((200, 200))
        self.screen.fill(self.color.white)
        draw_castle(self.screen, 10, 10, self.color.blue)
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.clock.tick(10)

    def testMakeRect(self):
        expect = (1, 3, 2, 2)
        result = make_rect(1, 3, 3, 1)
        self.assertEqual(result, expect)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()