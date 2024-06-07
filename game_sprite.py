"""
Author Paul Brace June 2024
Base object for Asteroid game sprites
"""

from pygame import Vector2, transform

class GameSprite():
    # Base object for game sprites
    def __init__(self, image, x, y):
        """
        :param image:   Default image for sprite
        :param x:       Position on screen
        :param y:
        """
        self._image = image
        self.width = self._image.get_width()
        self.height = self._image.get_height()
        self.radius = self.width / 2
        self.position = Vector2(x, y)
        # Amount to move on an update
        self.velocity = Vector2(0, 0)
        # Done is used to indicate that the object is finished with and can be deleted
        self.done = False

    def image(self):
        return self._image

    def set_image(self, value):
        self._image = value
        self.width = self._image.get_width()
        self.height = self._image.get_height()
        self.radius = self.width / 2

    def reduce_size(self, factor):
        self.set_image(transform.scale_by(self._image, factor))

    def update(self):
        # Move object
        self.position += self.velocity

    def draw(self, screen):
        adj_position = self.position - Vector2(self._image.get_size()) * 0.5
        screen.blit(self._image, adj_position)

    def collide_rect(self, object):
        """
        :param object:
        :return: True if the rectangles of objects collide
        """
        return  abs(abs(self.position.x) - abs(object.position.x)) < self.width / 2 + object.width / 2 \
                and abs(abs(self.position.y) - abs(object.position.y)) < self.height / 2 + object.height / 2

    def collide_circle(self, object):
        """
        :param object:
        :return: True if the distance between self and the object
        is < the sum of the radius of the objects. I.e intersection of
        two imaginary circles with a radius of half the width of the objects
        less 2 so there is a small overlap
        """
        distance = self.position.distance_to(object.position)
        return distance < self.radius + object.radius - 2


