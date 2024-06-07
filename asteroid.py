"""
Author Paul Brace June 2024
Asteroid class for Asteroids Game
"""
import random

from pygame import *
from constants import *
from game_sprite import GameSprite
from sprite_list import SpriteList
from explosion import Explosion

asteroids = SpriteList()
asteroid_image = image.load('images/asteroid.png')
asteroid_hit = mixer.Sound('sounds/strike.wav')
# divisor to restrict speed
SPEED = 500
# vector pointing up
UP = Vector2(0, 1)
# score for hitting asteroids based on size
SCORE = [200, 150, 100, 50]

class Asteroid(GameSprite):
    def __init__(self, x, y, player_position, size):
        # size -1 = random else 0 to 3 indicates size to set
        if size == -1:
            # use a random float as gives better randomness than randint
            size = random.random()
            if size < .26:
                self.size = AST_TINY
            elif size < .51:
                self.size = AST_SMALL
            elif size < .76:
                self.size = AST_MED
            else:
                self.size = AST_LARGE
        else:
            self.size = size
        image = transform.scale_by(asteroid_image, (self.size + 1) * 0.25)
        super().__init__(image, x, y)
        # set to True when asteroid hit
        self._hit = False
        # Amount to move asteroid in x and y axis when update called
        dx = (player_position.x - x) / SPEED
        dy = (player_position.y - y) / SPEED
        self.velocity = Vector2(dx, dy)
        # Angle of rotation to spin asteroid
        self.angle = 0
        self.spin_speed = random.random() * 2
        if random.random() > 0.5:
            self.spin_speed *= -1
        # Add to list of asteroids
        asteroids.add(self)

    def update(self):
        # if hit then reduce size
        if self._hit:
            self.reduce_size(0.95)
            if self.size == AST_MED and self.width <= 60:
                self._hit = False
            elif self.size == AST_SMALL and self.width <= 40:
                self._hit = False
            elif self.size == AST_TINY and self.width <= 20:
                self._hit = False
            elif self.size == AST_NONE and self.width <= 2:
                self.done = True
        # move asteroid
        self.position = self.position + self.velocity
        # Check if moved off screen
        if self.position.x > WIDTH + 100 or self.position.x < 0 - 100 or \
            self.position.y > HEIGHT + 100 or self.position.y < 0 - 100:
            self.done = True

    def draw(self, screen):
        # Rotate asteroid as it moves
        self.angle += self.spin_speed
        rotated_surface = transform.rotozoom(self.image(), self.angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        adj_position = self.position - rotated_surface_size * 0.5
        screen.blit(rotated_surface, adj_position)

    def hit(self):
        """
        :return: score for hitting asteroid
        """
        if not self._hit:
            self._hit = True
            score = SCORE[self.size]
            self.size -= 1
            Explosion(self.position.x, self.position.y, (self.size + 2) * 15, "grey", 0.025)
            asteroid_hit.play()
            if self.size > AST_TINY:
                # break off segments
                for i in range(self.size):
                    direction = Vector2(random.randint(0, WIDTH * 2), random.randint(0, HEIGHT * 2))
                    Asteroid(self.position.x, self.position.y, direction, 0)
            return score
        else:
            return 0

