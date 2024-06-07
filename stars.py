"""
Author Paul Brace June 2024
Star class use to produce a star field where you are flying upwards
for Asteroids game
"""

import pygame.draw
import random
from constants import *

star_list = []

def initialize_stars():
    """creates a new starfield"""
    if len(star_list) == 0:
        for x in range(NUMSTARS):
            star = Star(
                random.randint(10, WIDTH - 10),
                random.randint(0, HEIGHT),
                random.randint(1, 3)
            )
            star_list.append(star)

def clear_stars():
    star_list.clear()

def move_stars(screen):
    for star in star_list:
        star.move()
        star.draw(screen)

class Star:
    # create star class
    def __init__(self, x, y, radius):
        """ initialise star at x, y center and to move down screen """
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0.5)
        self.radius = radius

    def move(self):
        """ move star
            If reached edge of screen then reinitialise """
        self.position += self.velocity
        # if star has reached the edge of the screen then reenter at top of screen
        if self.position.y > HEIGHT:
            self.position.y = 0

    def draw(self, screen):
        """ draw star by drawing a circle of self.radius """
        pygame.draw.circle(screen, 'white', self.position, self.radius)
