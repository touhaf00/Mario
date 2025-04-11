import pygame
from config import SCREEN_HEIGHT, GRAVITY

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/mario.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 300
        self.vel_y = 0
        self.health = 3
        self.facing = 1
        self.invulnerable = False
        self.invulnerable_timer = 0

    def update(self, platform_group):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.facing = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.facing = 1

        if self.facing == -1:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.handle_collisions(platform_group)

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                print(f"[DEBUG] Mario is no longer invulnerable at position {self.rect.topleft}")

    def handle_collisions(self, platform_group):
        for platform in platform_group:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0

    def jump(self):
        if self.vel_y == 0:
            self.vel_y = -15
