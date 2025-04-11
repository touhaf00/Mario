import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, world_width, world_height):
        self.camera = pygame.Rect(0, 0, world_width, world_height)
        self.world_size = (world_width, world_height)
        self.bounds = (0, 0, world_width, world_height)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Clamp so the camera doesn't go outside the world boundaries
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_size[0] - SCREEN_WIDTH), x)
        y = max(-(self.world_size[1] - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.bounds[2], self.bounds[3])
