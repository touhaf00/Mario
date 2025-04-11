import pygame
from config import *

class Enemy(pygame.sprite.Sprite):
    _id_counter = 0

    def __init__(self, x, y, speed, patrol_range):
        super().__init__()
        self.id = Enemy._id_counter
        Enemy._id_counter += 1
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.vel_y = 0
        self.dead = False
        # La variable patrol_range n'est plus utilisée ici puisque nous utilisons
        # les bords de la plateforme pour la limitation. Vous pouvez la conserver pour d'autres usages.
        self.patrol_range = patrol_range

    def update(self, platforms):
        # Appliquer la gravité
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        current_platform = None
        # Détecter la plateforme sur laquelle l’ennemi se trouve
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                # Positionner l'ennemi juste au-dessus de la plateforme
                self.rect.bottom = platform.rect.top + 5
                self.vel_y = 0
                current_platform = platform
                break

        if current_platform:
            margin = 5  # Marge de sécurité pour éviter de toucher les bords
            # Définir les bornes de déplacement en fonction de la plateforme
            left_bound = current_platform.rect.left + margin
            right_bound = current_platform.rect.right - margin - self.rect.width

            # Déplacement horizontal
            self.rect.x += self.speed

            # Si l'ennemi dépasse les bornes, le replacer sur la borne et inverser la direction
            if self.rect.x < left_bound:
                self.rect.x = left_bound
                self.speed = -self.speed
            elif self.rect.x > right_bound:
                self.rect.x = right_bound
                self.speed = -self.speed
        else:
            # Si l'ennemi n'est sur aucune plateforme, il continue simplement son déplacement horizontal
            self.rect.x += self.speed

    def kill(self):
        self.dead = True
        print(f"[DEBUG] Enemy ID {self.id} killed at position: {self.rect.topleft}")
        super().kill()
