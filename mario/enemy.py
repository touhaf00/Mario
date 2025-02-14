import pygame
from config import *
import random

class Enemy(pygame.sprite.Sprite):
    _id_counter = 0

    def __init__(self, x, y, speed):
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

    def update(self, platforms):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:

                self.rect.bottom = platform.rect.top + 5
                self.vel_y = 0

        # Move horizontally.
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.speed = -self.speed  # Reverse direction when off-screen.

    def kill(self):
        self.dead = True
        print(f"[DEBUG] Enemy ID {self.id} killed at position: {self.rect.topleft}")
        super().kill()
