import pygame
from .sprites import ship_1


class Rocket(pygame.sprite.Sprite):

    def __init__(self, pos=pygame.math.Vector2(0, 0), direction: float = 0, image_path = ship_1):
       
       # Call the parent class (Sprite) constructor
       super().__init__()

       # Make sure objects are of the right type
       self.pos = pygame.math.Vector2(pos)
       self.velocity = pygame.math.Vector2(0, 0)
       self._direction = float(direction)
       self.image = None

       self._original_image = pygame.image.load(image_path).convert_alpha()

    def update(self, *args, dt=0, screen_dimensions=None, **kwargs):
        assert screen_dimensions, "screen_dimensions is required"

        screen_x_min, screen_y_min, screen_x_max, screen_y_max = screen_dimensions

        if self.pos.y < screen_y_min:
            self.velocity.y = abs(self.velocity.y)
        elif self.pos.y > screen_y_max:
            self.velocity.y = -abs(self.velocity.y)

        if self.pos.x < screen_x_min:
            self.velocity.x = abs(self.velocity.x)
        elif self.pos.x > screen_x_max:
            self.velocity.x = -abs(self.velocity.x)

        self.pos += self.velocity * dt

        if self.image is None:
            self.image = pygame.transform.rotate(self._original_image, self._direction)
            self.rect = self.image.get_rect()

        self.rect.center = self.pos

    def rotate(self, degrees):
        self._direction += degrees
        self.image = None

    def fire(self, thrust=0.01):
        thrust_vector = pygame.math.Vector2(0, -thrust)
        thrust_vector = thrust_vector.rotate(-self._direction)
        self.velocity += thrust_vector


