import pygame
class Platform(pygame.sprite.Sprite):
    all_platforms = []

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Platform.all_platforms.append(self)

    @staticmethod
    def update_all():
        pass

    @staticmethod
    def draw_all(screen):
        for platform in Platform.all_platforms:
            screen.blit(platform.image, platform.rect)