import pygame


class Planet(pygame.sprite.Sprite):

    def __init__(self, pos=pygame.math.Vector2(0, 0), mass=1e3, radius=10, colour="white"):
       
       # Call the parent class (Sprite) constructor
       super().__init__()

       # Make sure objects are of the right type
       self.pos = pygame.math.Vector2(pos)
       self.mass = float(mass)
       self.radius = int(radius)
       self.colour = colour

       diameter = 2 * self.radius

       # Create our planet "image" - we must make sure the image is transparent - we could also load a drawing
       self.image = pygame.Surface([diameter, diameter], pygame.SRCALPHA)
       self.image = self.image.convert_alpha()
       self.image.fill((0, 0, 0, 0))
       pygame.draw.circle(self.image, color=self.colour, center=(radius, radius), radius=radius, width=radius)

       # This is our boundary box
       self.rect = self.image.get_rect()
       self.rect.center = self.pos
