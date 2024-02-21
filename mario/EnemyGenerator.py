import pygame
import random
import Mario
import Plateform
import Enemy

class EnemyGenerator:
    def __init__(self, screen_width, enemy_y, enemy_speed, spawn_delay, scale):
        self.screen_width = screen_width
        self.enemy_y = enemy_y  # Fixed Y position for all enemies
        self.enemy_speed = enemy_speed
        self.spawn_delay = spawn_delay
        self.scale = scale
        self.enemies = pygame.sprite.Group()
        self.last_spawn_time = 0

    def update(self):
        self.enemies.update()
        self.spawn_enemy()

        # Draw enemies
        for enemy in self.enemies:
            enemy.update()
            enemy.update_position()

            # Check if the enemy is below the screen, set is_life to False
            if enemy.rect.y > 600:
                enemy.is_life = False

    def draw(self, screen):
        self.enemies.draw(screen)

    def draw(self, screen):
        self.enemies.draw(screen)

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            enemy = Enemy(self.screen_width, self.enemy_y, self.enemy_speed, self.scale)
            self.enemies.add(enemy)
            self.last_spawn_time = current_time