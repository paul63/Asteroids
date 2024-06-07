"""
Author Paul Brace June 2024
Explosion class for Asteroids game
"""

from pygame import *
import random
from sprite_list import SpriteList

explosions = SpriteList()

class Explosion:
    def __init__(self, x_pos, y_pos, size, color, rate):
        """
        :param x_pos:   Position on screen
        :param y_pos:
        :param size:    Number of particles to create is * by 2
        :param color:   Color of particles
        :param rate:    Rate of dissipation (particles reduce in size) of particles
        """
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.color = color
        self.rate = rate
        self.done = False
        self.particles = []
        # Create particles
        self.explode()
        # Add to list of explosions
        explosions.add(self)

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.done:
                self.particles.remove(particle)
        if len(self.particles) == 0:
            self.done = True

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def explode(self):
        # Create an explosion effect
        # create particles of random size and direction
        for i in range(0, self.size * 2):
            self.particles.append(Particle(self.x, self.y,
                                           random.random() * 4,
                                           self.color,
                                           (random.random() - 0.5) * random.random() * 6,
                                           (random.random() - 0.5) * random.random() * 6,
                                           self.rate))


# Rate at which particles slow down
FRICTION = 0.99
class Particle:
    def __init__(self, x, y, radius, color, velocity_x, velocity_y, rate):
        self.position = Vector2(x, y)
        self.radius = radius
        self.color = color
        self.velocity = Vector2(velocity_x, velocity_y)
        self.rate = rate
        self.done = False

    def draw(self, screen):
        draw.circle(screen, self.color, self.position, self.radius)

    def update(self):
        self.velocity *= FRICTION
        if self.radius > 0:
            self.radius -= self.rate
        if self.radius <= 0:
            self.done = True
        if not self.done:
            self.position += self.velocity
