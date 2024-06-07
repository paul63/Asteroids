"""
Author Paul Brace June 2024
Player class for Asteroids Game
"""
import random

from pygame import *
from constants import *
from game_sprite import GameSprite
from explosion import Explosion

player_hit = mixer.Sound('sounds/lifeLost.wav')
player_image = image.load('images/player.png')
thrust_image = image.load('images/thrust.png')
# Speed of rotation
SPEED = 4
# Number of frames between bullet firing
BULLET_RATE = 20
# Hyper jump interval
HYPER_JUMP = 60
# Thrust duration
THRUST = 30
# Vector pointing up
UP = Vector2(0, 1)

class Player(GameSprite):
    def __init__(self, ):
        """ initialise positioned bottom center """
        super().__init__(player_image, WIDTH / 2, HEIGHT / 2)
        # When the player shoots, timer is set to RELOAD_TIME - it then counts
        # down - when it reaches zero the player can shoot again
        # Also used to display player hit image for a few seconds
        self.timer = -1
        # alive is set to false when player hit
        self.alive = True
        # done tells main that shrt display time is up after player has been hit
        # and player can be reset
        self.done = False
        # vector for rotation and thrust
        self.direction = Vector2(UP)
        self.last_reverse = 0
        # timer to allow another bullet to be released
        self._bullet_release = BULLET_RATE
        # Thrust control
        self._thrust = 0
        # Jump allowed timer
        self.last_jumped = 0

    def hit(self):
        """ player hit so set state
            timer use changed to keep on screen during explosion """
        player_hit.play()
        self.alive = False
        self.timer = -1
        Explosion(self.position.x, self.position.y, 100, "red", 0.025)

    def reset(self):
        # Reset for next life
        self.alive = True
        self.done = False
        self.timer = -1
        self.direction = Vector2(UP)
        self.position.x = WIDTH / 2
        self.position.y = HEIGHT / 2
        self.last_reverse = 0


    def rotate(self, clockwise=True):
        # Rotate player when keyboard instructions used
        sign = 0.5 if clockwise else -0.5
        angle = SPEED * sign
        self.direction.rotate_ip(angle)

    def set_direction(self, pos):
        # Set player to point in directions of pos (will be mouse position)
        adj_pos = (self.position.x - pos[0], self.position.y - pos[1])
        self.direction.rotate_ip(self.direction.angle_to(Vector2(adj_pos)))

    def thrust(self):
        # Set thrust used to move player
        self._thrust = THRUST

    def hyper_jump(self):
        # Move player to a random position
        if self.last_jumped <= 0:
            self.position.x = random.randint(20, WIDTH - 20)
            self.position.y = random.randint(20, HEIGHT - 20)
            self.last_jumped = HYPER_JUMP  # 1 second between allowed jumps

    def bullet_released_timer(self):
        # Set when a bullet released
        self._bullet_release = BULLET_RATE

    def get_bullet_release(self):
        return self._bullet_release

    def update(self):
        """ check if a key has been pressed and act accordingly
            count timer for firing interval
            if player presses space then returns FIRE """
        fire = False
        # reduce timers
        if self.last_reverse > 0:
            self.last_reverse -= 1
        if self._bullet_release > 0:
            self._bullet_release -= 1
        if self.last_jumped > 0:
            self.last_jumped -= 1
        if self.alive:
            keys = key.get_pressed()
            if keys[K_LEFT]:
                # rotate left
                self.rotate(clockwise=False)
            if keys[K_RIGHT]:
                # rotate right
                self.rotate(clockwise=True)
            if keys[K_UP]:
                # Move player
                self.thrust()
            if keys[K_h]:
                # Hyper jump if allowed
                self.hyper_jump()
            if keys[K_DOWN]:
                # reverse direction
                if self.last_reverse <= 0:
                    self.direction.rotate_ip(180)
                    self.last_reverse = 15
            if keys[K_SPACE] and self._bullet_release == 0:
                # fire a bullet
                fire = FIRE
                self.bullet_released_timer()
            self.timer -= 1
        else:
            # Timer countdown to keep on screen after being hit
            self.timer += 1
            if self.timer > DELAY * 2:
                self.done = True
        if self._thrust > 0:
            # In thrust mode so move player but gradually reduce velocity
            self.position -= self.direction * self._thrust / 5
            self._thrust -= 1
            # Check if moved off screen - enter at other edge
            if self.position.x > WIDTH:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.w = WIDTH
            if self.position.y > HEIGHT:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = HEIGHT
        return fire

    def draw(self, screen):
        if self.alive:
            # Select image based on trust state
            if self._thrust > 0:
                image = thrust_image
            else:
                image = self.image()
            angle = self.direction.angle_to(UP)
            rotated_surface = transform.rotozoom(image, angle, 1.0)
            rotated_surface_size = Vector2(rotated_surface.get_size())
            adj_position = self.position - rotated_surface_size * 0.5
            screen.blit(rotated_surface, adj_position)
