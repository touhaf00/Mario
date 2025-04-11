import pygame
from config import GRAVITY

class Enemy(pygame.sprite.Sprite):
    _id_counter = 0

    def __init__(self, x, y, speed, patrol_range):
        super().__init__()
        self.id = Enemy._id_counter
        Enemy._id_counter += 1
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.vel_y = 0
        self.dead = False
        self.patrol_range = patrol_range
        self.start_x = x

    def update(self, platforms):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        current_platform = None
        # Check collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top + 5
                self.vel_y = 0
                current_platform = platform
                break

        if current_platform:
            margin = 5
            left_bound = current_platform.rect.left + margin
            right_bound = current_platform.rect.right - margin - self.rect.width

            # Horizontal movement with patrol limits
            self.rect.x += self.speed
            # Reverse if at patrol boundaries (or platform boundaries)
            if (self.rect.x < left_bound) or (self.rect.x > right_bound):
                self.speed = -self.speed
                self.rect.x += self.speed  # adjust position after reversing
        else:
            self.rect.x += self.speed

    def kill(self):
        self.dead = True
        print(f"[DEBUG] Enemy ID {self.id} killed at position: {self.rect.topleft}")
        super().kill()
