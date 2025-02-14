import pygame
from enemy import Enemy
from plateform import Platform
import random

class EnemyGenerator:
    def __init__(self, screen_width, spawn_delay):
        self.screen_width = screen_width
        self.spawn_delay = spawn_delay
        self.enemies = pygame.sprite.Group()
        self.last_spawn_time = pygame.time.get_ticks()

    def create_enemy(self):
        platform = random.choice(Platform.all_platforms)
        x = self.screen_width
        y = platform.rect.y - 50  
        speed = random.randint(1, 3)
        return Enemy(x, y, speed)

    def update(self, platforms):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            enemy = self.create_enemy()
            self.enemies.add(enemy)
            self.last_spawn_time = current_time

        self.enemies.update(platforms)

    def draw(self, screen):
        self.enemies.draw(screen)
