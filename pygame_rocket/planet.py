import pygame
from .sprites import planet_1

class Planet(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0)):
       
       # Call the parent class (Sprite) constructor
       super().__init__()

       # Make sure objects are of the right type
       self.pos = pygame.math.Vector2(pos)

       self.image = pygame.image.load(planet_1).convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.center = self.pos
