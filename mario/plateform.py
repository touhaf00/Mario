import pygame

class Platform(pygame.sprite.Sprite):
    # Liste statique pour garder la référence de toutes les plateformes
    all_platforms = []

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Ajout de la plateforme à la liste statique
        Platform.all_platforms.append(self)
