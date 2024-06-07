"""
Author Paul Brace June 2024
Bullet class for Asteroids game
"""

from pygame import *
from game_sprite import GameSprite
from sprite_list import SpriteList
from constants import *

# multiplyer for number of pixels to move per update
bullet_speed = 5
bullet_image = image.load('images/bullet.png')
bullet_released = mixer.Sound('sounds/bullet.wav')
# Vector pointing up
UP = Vector2(0, 1)

bullets = SpriteList()

class Bullet(GameSprite):
    def __init__(self, position, velocity):
        # initialise bullet and set direction
        super().__init__(bullet_image, position.x, position.y)
        self.direction = Vector2(velocity)
        self.velocity = Vector2(velocity * bullet_speed)
        self.velocity.rotate_ip(180)
        # Move forward to appears from front of spaceship
        self.position += self.velocity * 5
        angle = self.direction.angle_to(UP)
        self.set_image(transform.rotozoom(self.image(), angle, 1.0))
        bullet_released.play()
        # Add to list of bullets
        bullets.add(self)


    def update(self):
        """ move bullet  """
        self.position = self.position + self.velocity
        # Check if moved off screen
        if self.position.x > WIDTH or self.position.x < 0 or \
            self.position.y > HEIGHT or self.position.y < 0:
            self.done = True
