import pygame
from config import SCREEN_HEIGHT, GRAVITY


class Mario(pygame.sprite.Sprite):
    def __init__(self, start_pos=(50, 300)):
        super().__init__()
        # Load the normal image, scaled to 50x50.
        self.normal_image = pygame.image.load("assets/mario.png").convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, (50, 50))
        # Create a powered-up version (bigger) – adjust size as desired.
        self.powered_image = pygame.transform.scale(self.normal_image, (75, 75))
        # Start with the normal image.
        self.image = self.normal_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos

        self.vel_y = 0
        self.health = 3
        self.facing = 1
        self.invulnerable = False
        self.invulnerable_timer = 0

        # Power-up attributes: when set, Mario is in "big" mode.
        self.powered_up = False
        self.power_up_timer = 0

    def update(self, platform_group):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.facing = -1
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.facing = 1

        # Select image based on whether Mario is powered up.
        if self.powered_up:
            self.image = self.powered_image
        else:
            self.image = self.normal_image

        # Flip the image if Mario is facing left.
        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Apply gravity and update vertical position.
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.handle_collisions(platform_group)

        # Process temporary invulnerability.
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                print(f"[DEBUG] Mario is no longer invulnerable at {self.rect.topleft}")

        # Process power-up timer.
        if self.powered_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.powered_up = False
                print("[DEBUG] Power-up wore off. Mario reverted to normal.")

    def handle_collisions(self, platform_group):
        for platform in platform_group:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0

    def jump(self):
        if self.vel_y == 0:
            # If powered up, jump higher.
            if self.powered_up:
                self.vel_y = -20
            else:
                self.vel_y = -15
