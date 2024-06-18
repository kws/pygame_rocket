import pygame

class GravityGroup(pygame.sprite.Group):

    @property
    def all_com(self):
        """
        Returns the centre of mass of all sprites in the group with a 'mass' attribute.
        """
        for s in self.sprites():
            if hasattr(s, "mass"):
                yield (*s.rect.center, s.mass)

    @property
    def centre_of_mass(self):
        """
        Calculates the combined centre of mass for the whole system.
        """
        coms = list(self.all_com)
        total_mass = sum(m for *_, m in coms)
        if total_mass == 0:
            return pygame.math.Vector2(0, 0)
        return (
            sum(x * m for x, _, m in coms) / total_mass,
            sum(y * m for _, y, m in coms) / total_mass,
            total_mass
        )
