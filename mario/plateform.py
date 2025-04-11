import pygame

class Platform(pygame.sprite.Sprite):
    # Static list to hold all platform instances, if needed
    all_platforms = []

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        Platform.all_platforms.append(self)
