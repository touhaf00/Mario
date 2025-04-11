import pygame
from config import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.world_size = (width, height)
        self.bounds = (0, 0, width, height)

    def apply(self, entity):
        """Retourne le rectangle de l'entité ajusté selon la position de la caméra."""
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Contraindre la caméra aux limites du monde
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_size[0] - SCREEN_WIDTH), x)
        y = max(-(self.world_size[1] - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.bounds[2], self.bounds[3])
